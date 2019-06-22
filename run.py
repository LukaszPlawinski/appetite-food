import os
import json
from flask import Flask, render_template,redirect,request,session, url_for
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId


# Connection with mongo db database

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["MONGO_DBNAME"] = "Appetite_food"
app.config["MONGO_URI"] = "mongodb+srv://root:r00tpassword@myfirstcluster-ggpfv.mongodb.net/Appetite_food?retryWrites=true&w=majority"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)


# Route for the main page. If Search button is clicked user is redirected to results.html
    
@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    
    if request.method == "POST":
        if request.form.get('action') == 'search':
            searched_text =  request.form.get('search_input')
            return redirect(url_for('search', 
                    search_text=searched_text))
    return render_template("index.html",
    recipes = mongo.db.recipes.find())
    

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form.get('username')})

        if existing_user is None:
            pw_hash = bcrypt.generate_password_hash(request.form['pass'])
            users.insert({'name' : request.form.get('username'), 'password' : pw_hash})
            session['username'] = request.form.get('username')
            return redirect(url_for('index'))
        return 'That username already exists!'
    return redirect(url_for('index'))

@app.route('/add_recipe')
def add_recipe():
   return render_template("add_recipe.html", 
   recipe =mongo.db.recipes.find())
   
#  This function takes all values from form about recipe and inserts them into mongo database
   
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    that_recipe = {
        "name": request.form.get('name'),
        "image": request.form.get('image'),
        "description": request.form.get('description'),
        "author": request.form.get('author'),
        "ingredient":  request.form.to_dict(flat=False)["ingredient_name"],
        "step":  request.form.to_dict(flat=False)["step_name"]
    }
    recipes.insert_one(that_recipe)
    return redirect(url_for('index'))
    
# Route wchich send us to meal.html page where are all details about choosen recipe

@app.route('/<recipe_id>')
def about_recipe(recipe_id):
    return render_template('meal.html',
    recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}))
    
# EDIT and UPDATE functions 
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db. recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('edit_recipe.html', recipe= the_recipe)

@app.route("/update_recipe/<recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        "name": request.form.get('name'),
        "image": request.form.get('image'),
        "description": request.form.get('description'),
        "author": request.form.get('author'),
        "ingredient":  request.form.to_dict(flat=False)["ingredient_name"],
        "step":  request.form.to_dict(flat=False)["step_name"]
    })
    return redirect(url_for('index'))


# DELETE function

@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('index'))
    
    
# SEARCH function takes searched phrase and rendering all recipes which contain this phrase in their name
    
@app.route("/search/<search_text>", methods=["GET","POST"])
def search(search_text):
    mongo.db.recipes.create_index([("name",'text')])
    query = ({ "$text": { "$search":search_text}})
    return  render_template("results.html",
    recipes=mongo.db.recipes.find(query))
    
# Contact form

@app.route("/contact")
def contact():
    return render_template("contact.html")
    
if __name__=='__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
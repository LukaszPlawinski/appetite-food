import os
import json
from flask import Flask, render_template,redirect,request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = "Appetite_food"
app.config["MONGO_URI"] = "mongodb+srv://root:r00tpassword@myfirstcluster-ggpfv.mongodb.net/Appetite_food?retryWrites=true&w=majority"

mongo = PyMongo(app)


    
@app.route("/")
def index():
     return render_template("index.html",
     recipes = mongo.db.recipes.find())
    
@app.route('/add_recipe')
def add_recipe():
   return render_template("add_recipe.html", 
   recipe =mongo.db.recipes.find())
   
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    that_recipe = {
        "name": request.form.get('name'),
        "image": request.form.get('image'),
        "description": request.form.get('description'),
        "ingredient":  request.form.to_dict(flat=False)["ingredient_name"],
        "step":  request.form.to_dict(flat=False)["step_name"]
    }
    recipes.insert_one(that_recipe)
        
    return redirect(url_for('index'))
    
    
@app.route('/<recipe_id>')
def about_recipe(recipe_id):
    return render_template('meal.html',
    recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}))
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db. recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('edit_recipe.html', recipe= the_recipe)

@app.route("/recipes")
def recipes():
    return render_template("recipes.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
    
if __name__=='__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
'''
    Table of Contents

    1. Connection with mongo db database
    2. Mail configuration
    3. MAIN page
    4. LOGIN function
    5. REGISTER function
    6. Check users in session before each request
    7. LOGOUT function
    8. ADD RECIPE page
    9. INSERT RECIPE
    10. MEAL page
    11. EDIT recipe  function
    12. UPDATE recipe function
    13. DELETE recipe function
    14. SEARCH function
    15. CHOSE CATEGORY
    16. CONTACT FORM

'''






import os
import json
from flask import Flask, render_template,redirect,request,session,g, url_for,flash
from flask_pymongo import PyMongo
import bcrypt
from bson.objectid import ObjectId
from flask_mail import Mail
from flask_mail import Message


# Connection with mongo db database

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["MONGO_DBNAME"] = "Appetite_food"
app.config["MONGO_URI"] = "mongodb+srv://root:r00tpassword@myfirstcluster-ggpfv.mongodb.net/Appetite_food?retryWrites=true&w=majority"
mongo = PyMongo(app)


# Mail configuration

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_DEFAULT_SENDER="appetitefoodinfo@gmail.com",
    MAIL_USERNAME =os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    )
mail = Mail(app)


# MAIN page. 
    
@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # when  search button is clicked user is redirected to results.html
        if request.form.get('action') == 'search':
            searched_text =  request.form.get('search_input')
            # if input is empty error alert apears
            if searched_text == "":
                flash("Please enter text to search","alert")
                return redirect(url_for('index',
                                        user=g.user))
            else:
                return redirect(url_for('search', 
                                        search_text=searched_text))
                            
        # redirect user to result.html page after category is changed
        else:
            choosen_category =  request.form.get('category_name')
            return redirect(url_for('chose_category', 
                                    choosen_category=choosen_category))
                    
    return render_template("index.html",
    recipes = mongo.db.recipes.find(),
    categories= mongo.db.categories.find(),
    user=g.user)


# LOGIN function

@app.route('/login', methods = ['GET','POST'])
def login():
    users = mongo.db.users
    the_user = request.form.get('username')
    login_user = users.find_one({'name' : the_user })
    # Password verification
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form.get('username')
            flash('Welcome {}'.format(the_user),'alert')
            return redirect(url_for('index'))
        else:
            flash('Invalid password !','alert')
            return redirect(url_for('index'))
    else:
        flash('Invalid username !','alert')
        return redirect(url_for('index'))

  
# REGISTER function

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form.get('username')})
        
        # Hashing password to don't keep it in plain text
        if existing_user is None:
            pw_hash = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form.get('username'), 'password' : pw_hash})
            session['username'] = request.form.get('username')
        else:
            flash('That username already exists!','alert')
            return redirect(url_for('index'))
    flash('You have been successfully registered ')
    return redirect(url_for('index'))
    

# Check users in session before each request

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session['username']
        

# LOGOUT function

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out','alert')
    return redirect(url_for('index'))


# ADD RECIPE page

@app.route('/add_recipe')
def add_recipe():
    return render_template("add_recipe.html", 
                          recipe =mongo.db.recipes.find(),
                          user=g.user)
 
 
#  INSERT RECIPE
   
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    
    # It takes all values from form about recipe and inserts them into mongo database
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
    
    
# MEAL page

@app.route('/<recipe_id>')
def about_recipe(recipe_id):
    return render_template('meal.html',
                            recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}),
                            user=g.user)
 
    
# EDIT recipe  function
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db. recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('edit_recipe.html',
                            recipe= the_recipe,
                            user=g.user)

# UPDATE recipe function

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


# DELETE recipe function

@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('index'))
    
    
# SEARCH function
    
@app.route("/search/<search_text>", methods=["GET","POST"])
def search(search_text):
    
    # takes searched phrase and rendering all recipes which contain this phrase in their name
    mongo.db.recipes.create_index([("name","text")])
    query = ({ "$text": { "$search":search_text}})
    the_recipes = mongo.db.recipes.find(query)
    the_number = the_recipes.count()
    flash(' for word "{}" :'.format(search_text),'result')
    
    return  render_template("results.html",
                            categories= mongo.db.categories.find(),
                            recipes= the_recipes,
                            recipes_number = the_number,
                            user=g.user)
 
    
# CHOSE CATEGORY

@app.route("/chose/<choosen_category>", methods=["GET","POST"])
def chose_category(choosen_category):
    the_recipes = mongo.db.recipes.find({"category": choosen_category})
    the_number = the_recipes.count()
    flash("  in {} category:".format(choosen_category),'result')
    
    return  render_template("results.html",
                            categories= mongo.db.categories.find(),
                            recipes_number = the_number,
                            recipes= the_recipes,  user=g.user)
    
    
# CONTACT FORM

@app.route("/contact",methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name=request.form.get('name')
        email=message=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        
        # Message template which is sended to website owner email
        msg = Message("Message",
                      recipients=["appetitefoodinfo@gmail.com"])
        msg.html = " <p>Mail from :<strong> " + name + "</strong></p><p>" + message + "</p><p>My email: "+ email + "</p><p>My phone: " + phone +"</p>"
        mail.send(msg)
        flash("Thank you for your message {}. We will respond as soon as possible.".format(
            request.form["name"]
        ))
        
    return render_template("contact.html",
                            user=g.user)
    
    

 
if __name__=='__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
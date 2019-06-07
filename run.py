import os
import json
from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = "Appetite_food"
app.config["MONGO_URI"] = "mongodb+srv://root:r00tpassword@myfirstcluster-ggpfv.mongodb.net/Appetite_food?retryWrites=true&w=majority"

mongo = PyMongo(app)


    
@app.route("/")
def index():
     return render_template("index.html", recipes = mongo.db.recipes.find())
     
     
@app.route("/login")
def login():
    return render_template("login.html")


@app.route('/<recipe_id>')
def about_recipe(recipe_id):
    return render_template('meal.html',
    recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}))
    

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
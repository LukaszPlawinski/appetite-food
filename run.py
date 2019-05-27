import os
import json
from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/")
def index():
     data = []
     with open("Data/recipes.json","r") as json_data:
        data =json.load(json_data)
     return render_template("index.html", recipes = data)
    
@app.route("/login")
def login():
    return render_template("login.html")
@app.route('/<meal_name>')
def about_meal(meal_name):
    meal = {}
    
    with open("Data/recipes.json", "r") as json_data:
        data = json.load(json_data)
        for obj in data:
            if obj["id"] == meal_name:
                meal = obj
    
    return render_template("meal.html", meal=meal)
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
import os
import json
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def index():
    data = []
     with open("data/recipes.json","r") as json_data:
        data =json.load(json_data)
     return render_template("index.html",recipes = data)
    
@app.route("/login")
def login():
    return render_template("login.html")
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
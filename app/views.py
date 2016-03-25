from app import app 
from flask import render_template, url_for
from utils import *


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    return "this is logout page"

@app.route("/_edit/<regex(r'(?:[a-zA-Z0-9_-]+/?)'):param>")
def edit_wiki(param):
    return param


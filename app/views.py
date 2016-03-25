from app import app 
from flask import render_template, url_for
from utils import *


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return "this is signup page"

@app.route("/login")
def login():
    return "this is login page"

@app.route("/logout")
def logout():
    return "this is logout page"

@app.route("/_edit/<regex(r'(?:[a-zA-Z0-9_-]+/?)'):param>")
def edit_wiki(param):
    return param


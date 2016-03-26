from app import app, db, bcrypt
from flask import render_template, url_for, request, flash, redirect, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from models import User
from forms import SignUpForm 
# from utils import *


@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/_edit/<regex(r'(?:[a-zA-Z0-9_-]+/?)'):param>")
# def edit_wiki(param):
#     return param

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('logged_in', None)
    flash("You have logged out", "info")
    return redirect(url_for('index'))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")
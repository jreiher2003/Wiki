from app import app, db
from flask import render_template, url_for, request, flash, redirect
from flask.ext.login import login_user, logout_user, login_required, current_user
from models import Users, bcrypt
from utils import *


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None 
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form["username"]).first()
        print user
        if user is not None and bcrypt.check_password_hash(user.password, request.form["password"]):
            remember_me = request.form["remember"]
            login_user(user, remember_me)
            flash("You were just logged in!", "success")
            return redirect(url_for('index'))
        else:
            flash("You couldn't login.  Please try again", "danger")
            return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out", "info")
    return redirect(url_for('index'))

@app.route("/_edit/<regex(r'(?:[a-zA-Z0-9_-]+/?)'):param>")
def edit_wiki(param):
    return param


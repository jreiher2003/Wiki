from app import app, db, bcrypt
from flask import render_template, url_for, request, flash, redirect, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from models import User
from forms import SignUpForm 
from utils import *


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/_edit/<regex(r'(?:[a-zA-Z0-9_-]+/?)'):param>")
def edit_wiki(param):
    return param

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(name=request.form["username"]).first()
        if user is not None and user.password == request.form["password"]: 
            login_user(user)
            flash("you were signed in", "success")
            return redirect(url_for("index"))
        else:
            flash("invalid", "danger")
            return redirect(url_for("login"))
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
    if request.method == "POST":
        user = User(
            name=request.form["username"],
            email=request.form["email"],
            password=request.form["password"]
            )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("You just added user <strong>%s</strong>" % user.name, "success")
        return redirect(url_for('index'))
    return render_template("signup.html")
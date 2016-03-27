from app import app, db, bcrypt
from flask import render_template, url_for, request, flash, redirect, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from models import User
from forms import SignUpForm, LoginForm
from utils import *


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/_edit/<regex(r'(?:[a-zA-Z0-9_-]+/?)'):param>")
def edit_wiki(param):
    return param

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data): 
            login_user(user)
            flash("you were signed in", "success")
            return redirect(url_for("index"))
        else:
            flash("<strong>Invalid password.</strong> Please try again.", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", form=form, error=error)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("logged_in", None)
    flash("You have logged out", "info")
    return redirect(url_for("index"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data
            )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("You just added user <strong>%s</strong>" % user.name, "success")
        return redirect(url_for("index"))
    return render_template("signup.html", error=error, form=form)
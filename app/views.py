from app import app, db, bcrypt
from flask import render_template, url_for, request, flash, redirect, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from models import User, Wiki, WikiRevisions
from forms import SignUpForm, LoginForm, WikiForm
from utils import *
from functools import wraps




@app.route("/")
def index(page_name=None):
    wiki_posts = Wiki.query.order_by(Wiki.id.desc()).all()
    return render_template(
        "index.html", 
        wiki_posts=wiki_posts
        )

@app.route("/<path:page_name>", methods=["GET", "POST"])
def show_wiki(page_name):
    wiki_page = Wiki.query.filter_by(page_name=page_name).first()
    try:
        wiki_page.page_name
        return render_template(
          "show_wiki.html", 
            wiki_page=wiki_page
            )
    except AttributeError:
        return redirect(url_for('create_wiki_page', new_page=page_name))


# <regex(r'(?:[a-zA-Z0-9_-]+/?)'):new_page>/
@app.route("/_new/<path:new_page>", methods=["GET", "POST"])
@login_required
def create_wiki_page(new_page):
    form = WikiForm()
    if form.validate_on_submit():
        new_wiki = Wiki(
            page_name=new_page, 
            wiki_post=form.wiki_post.data,
            user_id=current_user.id
            )
        db.session.add(new_wiki)
        db.session.commit()
        wiki_rev = WikiRevisions(
            wiki_parent=new_wiki.id, 
            wiki_post_rev=form.wiki_post.data, 
            user_id=new_wiki.user_id
            )
        db.session.add(wiki_rev)
        db.session.commit()
        flash("You just created a new wiki named %s" % new_wiki.page_name, "info")
        return redirect(url_for("index"))
    return render_template(
        "create_wiki.html", 
        new_page=new_page, 
        form=form
        )




@app.route("/_edit/<page_name>/", methods=["GET", "POST"])
@login_required
def edit_wiki(page_name):
    wiki_page = Wiki.query.filter_by(page_name=page_name).one()
    form = WikiForm(obj=wiki_page)
    if form.validate_on_submit():
        wiki_page.wiki_post = form.wiki_post.data
        revisions = WikiRevisions(
            wiki_parent=wiki_page.id,
             wiki_post_rev=form.wiki_post.data, 
             user_id=current_user.id
             )
        db.session.add(revisions)
        db.session.add(wiki_page)
        db.session.commit()
        flash("you just edited wiki page %s" % wiki_page.page_name, "info")
        return redirect(url_for("show_wiki", page_name=page_name))
    return render_template(
        "edit_wiki.html", 
        form=form
        )


@app.route("/<page_name>/_history", methods=["GET", "POST"])
def show_history(page_name):
    wiki_page = Wiki.query.filter_by(page_name=page_name).one()
    revisions = WikiRevisions.query.filter_by(
        wiki_parent=wiki_page.id).order_by(
        WikiRevisions.id.desc()).all()
    return render_template(
        "history.html", 
        revisions=revisions
        )

 
@app.route("/new", methods=["GET", "POST"])
def create_page():
    return render_template("create_page.html")

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
    return render_template(
        "login.html", 
        form=form, 
        error=error
        )

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
    return render_template(
        "signup.html", 
        error=error, 
        form=form
        )
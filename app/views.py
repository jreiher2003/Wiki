from app import app, db, bcrypt # pragma: no cover
from flask import render_template, url_for, request, flash, redirect, session # pragma: no cover
from flask.ext.login import login_user, logout_user, login_required, current_user # pragma: no cover
from models import User, Wiki, WikiRevisions # pragma: no cover
from forms import SignUpForm, LoginForm, WikiForm # pragma: no cover
from utils import get_ip # pragma: no cover

@app.route("/")
def index():
    wiki_posts = Wiki.query.order_by(Wiki.id.desc()).all()
    wiki_rev = WikiRevisions.query.all()
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
        return redirect(url_for(
            "create_wiki_page", 
            new_page=page_name))

@app.route("/_new/<path:new_page>", methods=["GET", "POST"])
@login_required
def create_wiki_page(new_page):
    error = None
    form = WikiForm()
    if form.validate_on_submit():
        new_wiki = Wiki(
            page_name=new_page, 
            wiki_post=form.wiki_post.data,
            version=1,
            user_id=current_user.id
            )
        db.session.add(new_wiki)
        db.session.commit()
        wiki_rev = WikiRevisions(
            wiki_parent=new_wiki.id, 
            wiki_post_rev=form.wiki_post.data, 
            user_id=new_wiki.user_id,
            version=new_wiki.version,
            )
        db.session.add(wiki_rev)
        db.session.commit()
        flash("You just created a new wiki named <u>%s</u>" % new_wiki.page_name, "success")
        return redirect(url_for("index"))
    return render_template(
        "create_wiki.html", 
        new_page=new_page, 
        form=form,
        error=error
        )

@app.route("/_edit/<page_name>/", methods=["GET", "POST"])
@login_required
def edit_wiki(page_name):
    error = None
    wiki_page = Wiki.query.filter_by(page_name=page_name).one()
    form = WikiForm(obj=wiki_page)
    if form.validate_on_submit():
        wiki_page.wiki_post = form.wiki_post.data
        wiki_page.version += 1
        revisions = WikiRevisions(
            wiki_parent=wiki_page.id,
             wiki_post_rev=form.wiki_post.data, 
             user_id=current_user.id,
             version=wiki_page.version
             )
        db.session.add(revisions)
        db.session.add(wiki_page)
        db.session.commit()
        flash("You just edited wiki page <u>%s</u>" % wiki_page.page_name, "success")
        return redirect(url_for("show_wiki", page_name=page_name))
    return render_template(
        "edit_wiki.html", 
        form=form,
        wiki_page=wiki_page,
        error = error
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

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is not None and bcrypt.check_password_hash(
            user.password, form.password.data): 
            login_user(user)
            flash("You have signed in as <strong>%s</strong>!" % user.name, "success")
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
    session.pop("session", None)
    flash("You have logged out.", "danger")
    referer = request.headers["referer"]
    return redirect(referer)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data,
            ip=get_ip())
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("You just added user <strong>%s</strong>" % user.name, "success")
            return redirect(url_for("index"))
        except:
            flash("That username already exists", "danger")
            return redirect(url_for("signup"))
    return render_template(
        "signup.html", 
        error=error, 
        form=form
        )
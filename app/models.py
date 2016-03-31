import datetime
from app import db
from app import bcrypt 
from slugify import slugify

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String)
    ip = db.Column(db.String)
    wiki = db.relationship("Wiki")
    wiki_rev_u = db.relationship("WikiRevisions")

    def __init__(self, name, email, password, ip):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.ip = ip

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<name> {}'.format(self.name)

class Wiki(db.Model):

    __tablename__ = "wiki"

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, default=1, autoincrement=True)
    page_name = db.Column(db.String)
    wiki_post = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    user = db.relationship("User")
    wiki_rev = db.relationship("WikiRevisions")

    @property 
    def slug(self):
        return slugify(self.page_name)

    @property 
    def format_date(self):
        return '{dt:%A} {dt:%B} {dt.day}, {dt.year}'.format(dt=self.date_created)

    @property 
    def format_time(self):
        return '{dt:%I:%M %p}'.format(dt=self.date_created)

    @property 
    def last_modified_date(self):
        return '{dt:%Y-%m-%d}'.format(dt=self.date_modified)

    @property 
    def last_modified_time(self):
        return '{dt:%I:%M %p}'.format(dt=self.date_modified)

    def __repr__(self):
        return '<id> {}'.format(self.id)


class WikiRevisions(db.Model):

    __tablename__ = "wiki_rev" 

    id = db.Column(db.Integer, primary_key=True)
    wiki_parent = db.Column(db.Integer, db.ForeignKey("wiki.id"))
    version = db.Column(db.Integer,  default=1, autoincrement=True)
    wiki_post_rev = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    wiki = db.relationship(Wiki)
    user = db.relationship(User)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    @property 
    def format_date(self):
        return '{dt:%A} {dt:%B} {dt.day}, {dt.year}'.format(dt=self.date_created)

    @property 
    def format_time(self):
        return '{dt:%I:%M %p}'.format(dt=self.date_created)

    @property 
    def last_modified_date(self):
        return '{dt:%Y-%m-%d}'.format(dt=self.date_modified)

    @property 
    def last_modified_time(self):
        return '{dt:%I:%M %p}'.format(dt=self.date_modified)

    def __repr__(self):
        return '<id> {}'.format(self.id)

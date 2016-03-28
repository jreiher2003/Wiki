import datetime
from app import db
from app import bcrypt 

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String)
    post = db.relationship("Wiki", backref="post")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

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
    version = db.Column(db.Integer)
    page_name = db.Column(db.String)
    wiki_post = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())


    @property 
    def format_date(self):
        return '{dt:%A} {dt:%B} {dt.day}, {dt.year}'.format(dt=self.date_created)

   
    def __repr__(self):
        return '<id> {}'.format(self.id)
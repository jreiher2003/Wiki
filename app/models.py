from app import db
from app import bcrypt 

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String)

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

   

from app import db
from app import bcrypt 

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(80), nullable=False)
   

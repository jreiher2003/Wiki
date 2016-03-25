from app import db, bcrypt

class Users(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String)

    def __init__(self, username, email, password):
        self.username = username 
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
        return '<username> {}'.format(self.username)

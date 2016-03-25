from app import db 
from app.models import Users 

db.drop_all()
print "just dropped db"
db.create_all() 

db.session.add(Users(username="admin", email="ad@min.com", password="admin"))
db.session.add(Users(username="admin2", email="2ad@min.com", password="admin2"))
db.session.add(Users(username="admin3", email="3ad@min.com", password="admin3"))
print "just added a user"

db.session.commit()
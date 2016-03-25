from app import db 
from app.models import Users 

db.drop_all()
print "just dropped db"
db.create_all() 

db.session.add(Users(1, "admin" "ad@min.com", "admin"))
db.session.add(Users(2, "admin2" "2ad@min.com", "admin2"))
db.session.add(Users(3, "admin3" "3ad@min.com", "admin3"))
print "just added a user"

db.session.commit()
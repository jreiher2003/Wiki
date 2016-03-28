from app import db 
from app.models import User, Wiki

db.drop_all()
print "just dropped db"
db.create_all() 

db.session.add(User(name="admin", email="admin1@admin.com", password="admin"))
db.session.add(User(name="admin2", email="admin2@admin.com", password="admin2"))
db.session.add(User(name="admin3", email="admin3@admin.com", password='admin3'))
print "just added a user"

db.session.add(Wiki(wiki_post="this is a post", page_name="testpage", user_id=1, version=1))
db.session.add(Wiki(wiki_post="another test post", page_name="testpage2", user_id=1, version=1))
print "just added a wikipost"

db.session.commit()
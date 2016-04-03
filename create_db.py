from app import db 
from app.models import User, Wiki, WikiRevisions

db.drop_all()
print "just dropped db"
db.create_all() 

db.session.add(User(name="admin", email="admin1@admin.com", password="admin", ip="73.55.103.114"))
db.session.add(User(name="admin2", email="admin2@admin.com", password="admin2", ip="73.55.103.114"))
db.session.add(User(name="admin3", email="admin3@admin.com", password='admin3', ip="73.55.103.114"))
print "just added a user"

db.session.add(Wiki(content="this is a post", page_name="testpage", user_id=1))
db.session.add(Wiki(content="another test post", page_name="testpage2", user_id=1))
print "just added a wikipost"

db.session.add(WikiRevisions(wiki_parent=1, wiki_post_rev="this is a post", user_id=1))
# db.session.add(WikiRevisions(wiki_parent=1, wiki_post_rev="this is another revised post", user_id=1))
# db.session.add(WikiRevisions(wiki_parent=1, wiki_post_rev="this is yet another revised post", user_id=1))

db.session.add(WikiRevisions(wiki_parent=2, wiki_post_rev="another test post", user_id=2))
# db.session.add(WikiRevisions(wiki_parent=2, wiki_post_rev="post 2 bla blas yep yep revised", user_id=2))

db.session.commit()
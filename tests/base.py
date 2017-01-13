from flask.ext.testing import TestCase 
from app import app, db
from app.models import User, Wiki, WikiRevisions

class BaseTestCase(TestCase):
    """ A Base Test Case """ 

    def create_app(self):
        app.config.from_object("config.TestConfig") 
        return app 

    def setUp(self):
        """ set up db """
        db.create_all()
        user = User(
            name="Admin", 
            email="test@email.com", 
            password="password",
            ip="127.0.0.1"
            )
        wiki = Wiki(
            page_name="testpage", 
            content="test wiki post", 
            user_id=user.id,
            version=1
            )
        wiki_rev = WikiRevisions(
            wiki_parent=1,
            wiki_post_rev="test wiki post",
            user_id=user.id,
            version=wiki.version
            )
        db.session.add(user)
        db.session.add(wiki)
        db.session.add(wiki_rev)
        db.session.commit()

    def tearDown(self):
        """ remove session and drop the db""" 
        db.session.remove()
        db.drop_all()
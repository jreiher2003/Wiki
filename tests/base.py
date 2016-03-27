from flask.ext.testing import TestCase 
from app import app, db
from app.models import User 

class BaseTestCase(TestCase):
    """ A Base Test Case """ 

    def create_app(self):
        app.config.from_object("config.TestConfig") 
        return app 

    def setUp(self):
        """ set up db """
        db.create_all()
        one = User(name="Admin", email="test@email.com", password="password")
        db.session.add(one)
        db.session.commit()

    def tearDown(self):
        """ remove session and drop the db""" 
        db.session.remove()
        db.drop_all()
from flask.ext.testing import TestCase 
from app import app 

class BaseTestCase(TestCase):
    """ A Base Test Case """ 

    def create_app(self):
        app.config.from_object("config.TestConfig") 
        return app 

    def setUp(self):
        """ set up db """
        pass 

    def tearDown(self):
        """ remove session and drop the db""" 
        pass 
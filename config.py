import os 

class BaseConfig(object):
    DEBUG = False 
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class DevelopmentConfig(BaseConfig): 
    DEBUG = True 

class TestConfig(BaseConfig):
    DEBUG = True 
    TESTING = True 
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
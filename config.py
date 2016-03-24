import os 

class BaseConfig(object):
    DEBUG = False 


class DevelopmentConfig(BaseConfig): 
    DEBUG = True 

class TestConfig(BaseConfig):
    DEBUG = True 
    TESTING = True 
    
import os 

class BaseConfig(object):
    DEBUG = False 


class DevelopmentConfig(BaseConfig): 
    DEBUG = True 
from app import app 

import unittest

from flask.ext.script import Manager 

manager = Manager(app) 

@manager.command 
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    manager.run()
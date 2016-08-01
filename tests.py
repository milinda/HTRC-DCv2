import unittest
from flask import Flask
from flask_testing import TestCase
from sdg.models import db, VMHost, VMImage, VM, VMMode, VMState, User, Result, VMActivity 

class ModelsTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user(self):
        user = User('mpathira', 'mpathira@indiana.edu', 2, 2048, 12)
        db.session.add(user)
        db.session.commit()

        assert user in db.session

if __name__ == '__main__':
    unittest.main()
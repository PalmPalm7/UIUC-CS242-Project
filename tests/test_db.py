import unittest

from flask import Flask
from flask_testing import TestCase

from dashboard import create_app
from dashboard.models.base import db


class TestDB(TestCase):
    ## test alchemy url
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_db.db"
    TESTING = True

    def create_app(self):
        return create_app()

    ## call the create all on db
    def setUp(self):
        db.create_all()

    # call drop all operation on  db
    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()

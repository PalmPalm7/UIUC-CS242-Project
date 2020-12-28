import unittest

from flask import Flask
from flask_testing import TestCase
import requests
from flask import Flask
from flask_testing import LiveServerTestCase
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dashboard import create_app


class TestApp(LiveServerTestCase):

    def create_app(self):
        return create_app()

    def test_server_is_up_and_running(self):
        # check if server responsed with 200 status code
        response = requests.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
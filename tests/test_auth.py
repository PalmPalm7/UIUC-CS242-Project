from abc import ABC

import tweepy
from flask_testing import TestCase
from tweepy import API, OAuthHandler

from dashboard import create_app
from dashboard.models import TwitterClient


class TestAuth(TestCase, ABC):

    def create_app(self):
        self.twitterClient = TwitterClient()
        return create_app()

    # check if the object is initioalized and and does not throw exception
    def test_assert_client(self):
        self.twitterClient = TwitterClient()
        self.assertIsInstance(self.twitterClient, TwitterClient)
    ## the the class variables are initilized
    def test_assert_api(self):
        self.twitterClient = TwitterClient()
        self.assertIsInstance(self.twitterClient.api, tweepy.API)
    ## the the class variables are initilized
    def test_assert_auth(self):
        self.assertIsInstance(self.twitterClient.auth, OAuthHandler)

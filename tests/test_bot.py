from abc import ABC
from datetime import datetime

from flask_testing import TestCase
from dashboard import create_app
from dashboard.models import TwitterClient

# create api client
api = TwitterClient()
# get home timeline tweets
tweet = api.home_timeline()


class TestApi(TestCase, ABC):
    ## create app function retuns the app with context

    def create_app(self):
        return create_app()

    def test_assert_bot_like(self):
        # like the tweet with id
        status = api.like(tweet[0].id)
        print("Like :",status)
        # check id status of tweet is liked or npt
        self.assertEqual(status.favorited, True)

    def test_assert_bot_retweet(self):
        # like the tweet with id
        status = api.retweet(tweet[0].id)
        print("Retweet:",status)
        # check id status of tweet is retweeted or npt
        self.assertEqual(status.retweeted, True)

    def test_assert_bot_reply(self):
        # like the tweet with id
        status = api.reply(text="reply from test cases",id=tweet[0].id)
        print("Reply",status)
        # check if status  text is same as the reply or not
        self.assertEqual(status.text, "reply from test cases")

    def test_assert_bot_update_status(self):
        text="update status from from test cases at:"+str(datetime.utcnow())

        status = api.update_status(text=text)
        print("Update Status:",status)

        # check if status  text is same as the update text or not
        self.assertEqual(status.text,text)


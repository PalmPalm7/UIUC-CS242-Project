from datetime import datetime

import tweepy
from nltk import sentiment
from textblob import TextBlob
from tweepy import OAuthHandler

from ..models.base import db
from ..config import Config
from .users import User
from .tweets import Tweet
import time

class StreamListener(tweepy.StreamListener):

    def __init__(self):
        """
        Class constructor or initialization method.
        """
        # keys and tokens from the Twitter Dev Console
        # attempt authentication
        try:
            print("=============================")
            # create OAuthHandler object
            self.auth = OAuthHandler(Config.consumer_key, Config.consumer_secret)
            # set access token and secret
            self.auth.set_access_token(Config.access_token, Config.access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
            # initialization time
            self.time  = time.time()
            ## limit time in seconds
            self.limit = 60
        except:
            ## exception in authentication
            print("Error: Authentication Failed")

    ## on status function calls for every tweet in stream
    def on_status(self, tweet):
        ## check if time limit reached the return false it will stop streaming
        if time.time() - self.time > self.limit:
            print("1 Minute Done")
            return False

        print("stream api:" + tweet.text)
        author = tweet.author
        ## insert USer details in db
        user = User(id=author.id, name=author.name, screen_name=author.screen_name,
                    followers_count=author.followers_count, friends_count=author.friends_count,
                    listed_count=author.listed_count, created_at=author.created_at,
                    profile_image_url=author.profile_image_url, time=datetime.utcnow())

        try:
            print(user)
            user.save()
        except Exception as e:
            print("Error saving user", e)
            user.rollback()

        ## TextBlob
        text_blob = TextBlob(tweet.text)
        ## insert Tweet Detais in db
        t = Tweet(id=tweet.id, text=tweet.text, created_at=tweet.created_at, user_id=user.id,
                  retweet=tweet.retweet_count, time=datetime.utcnow(),sentiment_polarity=text_blob.sentiment.polarity,sentiment_subjectivity=text_blob.sentiment.subjectivity)
        print(t)
        try:
            t.save()
            t.rollback()
        except Exception as e:
            print("error saving tweet", e)
            db.session.rollback()

    ## on_error function if any issue/error comes it will fail
    def on_error(self, status_code):
        if status_code == 420:
            return False


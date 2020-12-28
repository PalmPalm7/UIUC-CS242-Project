import logging as logger
import re
import json
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from flask import Flask, render_template, request
from ..config import Config
logger.basicConfig(level="DEBUG")

class TwitterClient(object):
	"""
	Generic Twitter Class for sentiment analysis.
	"""

	def __init__(self):
		"""
		Class constructor or initialization method.
		"""
		# keys and tokens from the Twitter Dev Console

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(Config.consumer_key, Config.consumer_secret)
			# set access token and secret
			self.auth.set_access_token(Config.access_token, Config.access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except Exception as e:
			print("Error: Authentication Failed",e)

	## for like and dislike the tweets:
	def like(self,id):
		tweet = self.api.get_status(id)
		if not tweet.favorited:
			return tweet.favorite()
		return tweet

	def update_status(self,text):
		return self.api.update_status(status=text)

	def get_status(self,id):
		return self.api.get_status(id)

	def reply(self,text,id):
		return self.api.update_status(
			status=text,
			in_reply_to_status_id=id,
		)

	## for retweeting the tweets:
	def retweet(self, id):
		tweet = self.api.get_status(id)
		if not tweet.retweeted:
			return tweet.retweet()
		return tweet

	def get_tweet(self,id):
		tweet = self.api.get_status(id)
		return tweet

	## return home tweets /timeline/home in web
	def home_timeline(self,count=20):
		return self.api.home_timeline(count=count)

	## return details of the current user
	def me(self):
		return self.api.me()

	## returns retweets of user
	def retweets_of_me(self):
		return self.api.retweets_of_me()

	## returns user timeline
	def user_timeline(self):
		return self.api.user_timeline()
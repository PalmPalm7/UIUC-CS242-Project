import json

from flask import current_app, Blueprint, render_template, request
from textblob import TextBlob
from tweepy import OAuthHandler

from ..models.base import db
from ..models import User, Tweet, TwitterClient, StreamListener
from datetime import datetime
from datetime import timedelta
import tweepy
from sqlalchemy import desc,asc
from ..config import Config

bot = Blueprint('bot', __name__, url_prefix='/')
api = TwitterClient()

global_tweets=[]
@bot.route('/test', methods=['GET', 'POST'])
def test():
    public_tweets = api.home_timeline(count=5)
    print ("HOME_TIMELINE:", len(public_tweets))
    public_retweets = api.retweets_of_me()
    array=[]
    for t in public_tweets:
        print("tweet:==================================>", t)
        #print("retweet tweet:==================================>", t.retweet())
        array.append(t)
    global_tweets = public_tweets
    return "<br><br><hr><br>"+str(array)
# bot home page
@bot.route('/bot', methods=['GET', 'POST'])
def index():
    # creating object of TwitterClient Class
    public_tweets=[]
    public_retweets=[]
    try:
        ## get the home_timeline tweets with count 5
        ## it returns status objects array
        public_tweets = api.home_timeline(count=5)
        print("HOME_TIMELINE:",len(public_tweets))
        public_retweets = api.retweets_of_me()
        global_tweets = public_tweets
    except Exception as e:
        print("Error: ", e)
    return render_template('bot.html', tweets=public_tweets,retweets=public_retweets)

# get id of tweet and get tweet and return
@bot.route('/get_tweet/<id>',methods=['GET','POST'])
def get_tweet(id):
    return str(api.get_tweet(id))

# get id of tweet and get status and return
@bot.route('/get_status/<id>',methods=['GET','POST'])
def get_status(id):
    status = api.get_status(id)
    expended_url = 'https://twitter.com/'+status.user.screen_name+'/status/'+str(status.id)
    return {'id':status.id,'expended_url':expended_url}

# update the status make a tweet
@bot.route('/update_status',methods=['GET','POST'])
def update_status():
    print(request.args)
    text=request.args.get('text')
    status = api.update_status(text=text)
    expended_url = 'https://twitter.com/'+status.user.screen_name+'/status/'+str(status.id)
    return {'id':status.id,'expended_url':expended_url}

# reply to a tweet
@bot.route('/reply/<id>',methods=['GET','POST'])
def reply(id=''):
    print(request.args)
    text=request.args.get('text')
    status = api.reply(
     text=text,
        id=id,
    )
    expended_url = 'https://twitter.com/'+status.user.screen_name+'/status/'+str(id)
    return {'id':status.id,'expended_url':expended_url}


## return sthe json of  count of last 1 min tweets and users
@bot.route('retweet/<id>', methods=['GET', 'POST'])
def retweet(id=''):
    status = api.retweet(id)
    expended_url = 'https://twitter.com/'+status.user.screen_name+'/status/'+str(id)
    return {'id':status.id,'expended_url':expended_url}

## returns the total count of tweets and users in db
@bot.route('/like/<id>', methods=['GET', 'POST'])
def like(id=''):
    status = api.like(id)
    expended_url = 'https://twitter.com/'+status.user.screen_name+'/status/'+str(id)
    return {'id':status.id,'expended_url':expended_url}


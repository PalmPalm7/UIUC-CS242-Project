from flask import current_app, Blueprint, render_template
from textblob import TextBlob
from tweepy import OAuthHandler

from ..models.base import db
from ..models import User, Tweet, TwitterClient, StreamListener
from datetime import datetime
from datetime import timedelta
import tweepy
from sqlalchemy import desc,asc
from ..config import Config

main = Blueprint('main', __name__, url_prefix='/')
api = TwitterClient()


@main.route('/', methods=['GET', 'POST'])
def index():
    # creating object of TwitterClient Class
    try:
        ## get the home_timeline tweets with count 5
        ## it returns status objects array
        public_tweets = api.home_timeline(count=5)
        tweets = []
        for tweet in public_tweets:
            # print(tweet)
            # get the author
            author = tweet.author
            # insert new user from author details
            user = User(id=author.id, name=author.name, screen_name=author.screen_name,
                        followers_count=author.followers_count, friends_count=author.friends_count,
                        listed_count=author.listed_count, created_at=author.created_at,
                        profile_image_url=author.profile_image_url)

            try:
                # save user to db
                user.save()
            except Exception as e:
                ## as save failed rollback the transaction
                user.rollback()
                print("Error saving user", e)

            ## TextBlob
            text_blob = TextBlob(tweet.text)
            print("Analysis:",text_blob.sentiment)

            ## insert Tweet Detais in db
            t = Tweet(id=tweet.id, text=tweet.text, created_at=tweet.created_at, user_id=user.id,
                      retweet=tweet.retweet_count, time=datetime.utcnow(),
                      sentiment_polarity=text_blob.sentiment.polarity,
                      sentiment_subjectivity=text_blob.sentiment.subjectivity)

            try:
                ## save the tweet to db
                t.save()
            except Exception as e:
                ## if save fails rollback the transcton
                t.rollback()
                print("error saving tweet", e)
    except Exception as e:
        print("Error: ",e)

    ## return the last 100 tweets inserted into the db
    tweets = Tweet.query.order_by(desc(Tweet.time)).limit(100).all()
        ## return the last 100 users inserted into the db
    users = User.query.order_by(desc(User.time)).limit(100).all()
    #print(users)
    #print(tweets)
    ## render the index.html page with data and show in browser
    return render_template('index.html', tweets=tweets, users=users)


## return sthe json of  count of last 1 min tweets and users
@main.route('/count', methods=['GET', 'POST'])
def count():
    from_date = (datetime.utcnow() - timedelta(minutes=1))
    tweets_count = Tweet.query.filter(Tweet.time > from_date).count()
    users_count = User.query.filter(User.time > from_date).count()
    # print(tweets_count, users_count)
    return {"tweets_count": tweets_count, "users_count": users_count}


# returns the total count of tweets and users in db
@main.route('/total', methods=['GET', 'POST'])
def total():
    from_date = (datetime.utcnow() - timedelta(minutes=1))
    tweets_count = Tweet.query.count()
    users_count = User.query.count()
    # print(tweets_count, users_count)
    return {"tweets_count": tweets_count, "users_count": users_count}

# returns the last 100 tweets and users inserted to db
@main.route('/top100', methods=['GET', 'POST'])
def top100():
    from_date = (datetime.utcnow() - timedelta(minutes=1))
    tweets = Tweet.query.order_by(desc(Tweet.time)).limit(100).all()
    tweets_data = []
    for t in tweets:
        tmp = t.to_json()
        tweets_data.append(tmp)

    users = User.query.order_by(desc(User.time)).limit(100).all()
    users_data = []
    for u in users:
        tmp = u.to_json()
        users_data.append(tmp)
    # print(users_data)
    # print(tweets_data)
    return {"tweets": tweets_data, "users": users_data}


# return the count of last 10 seconds tweets and users
@main.route('/count_ten', methods=['GET', 'POST'])
def count_ten():
    from_date = (datetime.utcnow() - timedelta(seconds=10))
    tweets_count = Tweet.query.filter(Tweet.time > from_date).count()
    users_count = User.query.filter(User.time > from_date).count()
    # print(tweets_count, users_count)
    return {"tweets_count": tweets_count, "users_count": users_count}


# trigger fucntion to start the streaming
# it will call the StreanListiner class to_data function
@main.route('/stream', methods=['GET', 'POST'])
def stream():
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.api.auth, listener=stream_listener)
    stream.filter(track=["trump", "clinton", "hillary clinton", "donald trump", "corona", "virus", "coronavirus"],
                  is_async=False)
    return "stream done"


# get the current user details and tweets
@main.route('/user', methods=['GET', 'POST'])
def get_user():
    # creating object of TwitterClient Class
    try:
        user = api.me()
        retweets = api.retweets_of_me()
        user_timeline = api.user_timeline()
        home_timeline = api.home_timeline(count=10)
        print("retweets",home_timeline)
        return render_template('user.html', user=user, user_timeline=user_timeline, home_timeline=home_timeline,
                               retweets=retweets)
    except Exception as e:
        print("Error:",e)
        # if exception or rate limit fetech form db
        tweets = Tweet.query.order_by(desc(Tweet.time)).limit(100).all()
        # return dummy user as api not working
        user={
            'name':'Test Name',
            'screen_name':'test_name',
            'profile_banner_url':'#',
            'profile_image_url':'#',
            'followers_count': 0,
            'friends_count':0,
            'listed_count':0,
            'favourites_count':0
        }
        # render the user.html file and show in browers
        return render_template('user.html', user=user, user_timeline=[], home_timeline=tweets,
                               retweets=[])

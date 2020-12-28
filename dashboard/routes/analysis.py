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

analysis = Blueprint('analysis', __name__, url_prefix='/')
api = TwitterClient()


# return the analysis and percentage of all stored in db
@analysis.route('/analysis',methods=['GET','POST'])
def index():
    total_tweets = Tweet.query.count()
    total_users = Tweet.query.count()

    total_positive = Tweet.query.filter(Tweet.sentiment_polarity > 0.01).count()
    total_negative = Tweet.query.filter(Tweet.sentiment_polarity < -0.01).count()
    total_neutral = Tweet.query.filter(Tweet.sentiment_polarity > -0.01).filter(Tweet.sentiment_polarity < 0.01).count()
    positive = (total_positive/total_tweets)*100
    negative = (total_negative/total_tweets)*100
    neutral = (total_neutral/total_tweets)*100
    positive=int(round(positive))
    negative = int(round(negative))
    neutral = int(round(neutral))

    # get all positive tweets
    positive_tweets = Tweet.query.join(User, User.id==Tweet.user_id).filter(Tweet.user_id == User.id)\
        .filter(Tweet.sentiment_polarity > 0.01).order_by(desc(Tweet.time)).limit(10).all()
    # get all negative tweets
    negative_tweets = Tweet.query.join(User, User.id==Tweet.user_id).filter(Tweet.user_id == User.id)\
        .filter(Tweet.sentiment_polarity < 0.01).order_by(desc(Tweet.time)).limit(10).all()
    # get all neutral tweets
    neutral_tweets = Tweet.query.join(User, User.id==Tweet.user_id).filter(Tweet.user_id == User.id)\
        .filter(Tweet.sentiment_polarity < 0.01).filter(Tweet.sentiment_polarity > -0.01).order_by(desc(Tweet.time)).limit(10).all()
    return render_template('analysis.html',
                           total_tweets=total_tweets,total_users=total_users,total_positive=positive,total_neutral=total_neutral,
                           total_negative=total_negative,positive=positive,negative=negative,neutral=neutral,
                           positive_tweets=positive_tweets,negative_tweets=negative_tweets,neutral_tweets=neutral_tweets)


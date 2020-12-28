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

stream = Blueprint('stream', __name__, url_prefix='/')
api = TwitterClient()


# custome stram page with custom tags and keywords
@stream.route('/custom_stream', methods=['GET', 'POST'])
def custom_stream():
    # creating object of TwitterClient Class
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

    positive_tweets = Tweet.query.join(User, User.id==Tweet.user_id).filter(Tweet.user_id == User.id)\
        .filter(Tweet.sentiment_polarity > 0.01).order_by(desc(Tweet.time)).limit(10).all()
    negative_tweets = Tweet.query.join(User, User.id==Tweet.user_id).filter(Tweet.user_id == User.id)\
        .filter(Tweet.sentiment_polarity < 0.01).order_by(desc(Tweet.time)).limit(10).all()
    neutral_tweets = Tweet.query.join(User, User.id==Tweet.user_id).filter(Tweet.user_id == User.id)\
        .filter(Tweet.sentiment_polarity < 0.01).filter(Tweet.sentiment_polarity > -0.01).order_by(desc(Tweet.time)).limit(10).all()

    return render_template('stream.html',
                           total_tweets=total_tweets,total_users=total_users,total_positive=positive,total_neutral=total_neutral,
                           total_negative=total_negative,positive=positive,negative=negative,neutral=neutral,
                           positive_tweets=positive_tweets,negative_tweets=negative_tweets,neutral_tweets=neutral_tweets)

# returns the total count of tweets and users in db
@stream.route('/mytotal', methods=['GET', 'POST'])
def total():
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
    '''
    positive_tweets = Tweet.query.join(User, User.id==Tweet.user_id).filter(Tweet.user_id == User.id)\
        .filter(Tweet.sentiment_polarity > 0.01).order_by(desc(Tweet.time)).limit(10).all()
    negative_tweets = Tweet.query.join(User, User.id==Tweet.user_id).filter(Tweet.user_id == User.id)\
        .filter(Tweet.sentiment_polarity < 0.01).order_by(desc(Tweet.time)).limit(10).all()
    neutral_tweets = Tweet.query.join(User, User.id==Tweet.user_id).filter(Tweet.user_id == User.id)\
        .filter(Tweet.sentiment_polarity < 0.01).filter(Tweet.sentiment_polarity > -0.01).order_by(desc(Tweet.time)).limit(10).all()
    '''
    return {
        "total_tweets": total_tweets,
        "total_users": total_users,
        "total_positive": total_positive,
        "total_neutal": total_neutral,
        "total_negative": total_negative,
        "positive":positive,
        "neutral":neutral,
        "negative":negative
    }

# returns the last 100 tweets and users inserted to db
@stream.route('/mytop100', methods=['GET', 'POST'])
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

## return sthe json of  count of last 1 min tweets and users
@stream.route('/mycount', methods=['GET', 'POST'])
def count():
    from_date = (datetime.utcnow() - timedelta(minutes=1))
    total_tweets = Tweet.query.filter(Tweet.time > from_date).count()
    total_users = User.query.filter(User.time > from_date).count()
    if total_tweets==0:
        total_tweets=1

    total_positive = Tweet.query.filter(Tweet.time > from_date).filter(Tweet.sentiment_polarity > 0.01).count()
    total_negative = Tweet.query.filter(Tweet.time > from_date).filter(Tweet.sentiment_polarity < -0.01).count()
    total_neutral = Tweet.query.filter(Tweet.time > from_date).filter(Tweet.sentiment_polarity > -0.01).filter(Tweet.sentiment_polarity < 0.01).count()
    positive = (total_positive/total_tweets)*100
    negative = (total_negative/total_tweets)*100
    neutral = (total_neutral/total_tweets)*100
    positive=int(round(positive))
    negative = int(round(negative))
    neutral = int(round(neutral))

    # print(tweets_count, users_count)
    return {"tweets_count": total_tweets, "users_count": total_users,"positive":positive,"negative":negative,"neutral":neutral}



# return the count of last 10 seconds tweets and users
@stream.route('/mycount_ten', methods=['GET', 'POST'])
def count_ten():
    from_date = (datetime.utcnow() - timedelta(seconds=10))
    total_tweets = Tweet.query.filter(Tweet.time > from_date).count()
    total_users = User.query.filter(User.time > from_date).count()
    if total_tweets==0:
        total_tweets=1

    total_positive = Tweet.query.filter(Tweet.time > from_date).filter(Tweet.sentiment_polarity > 0.01).count()
    total_negative = Tweet.query.filter(Tweet.time > from_date).filter(Tweet.sentiment_polarity < -0.01).count()
    total_neutral = Tweet.query.filter(Tweet.time > from_date).filter(Tweet.sentiment_polarity > -0.01).filter(Tweet.sentiment_polarity < 0.01).count()
    positive = (total_positive/total_tweets)*100
    negative = (total_negative/total_tweets)*100
    neutral = (total_neutral/total_tweets)*100
    positive=int(round(positive))
    negative = int(round(negative))
    neutral = int(round(neutral))

    # print(tweets_count, users_count)
    return {"tweets_count": total_tweets, "users_count": total_users,"positive":positive,"negative":negative,"neutral":neutral}


# trigger fucntion to start the streaming
# it will call the StreanListiner class to_data function
@stream.route('/custom_stream_start', methods=['GET', 'POST'])
def custom_stream_start():
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.api.auth, listener=stream_listener)
    track = request.args.get('tracks')
    print("tracks",track)
    if track is None or len(track)<2:
        track = ["trump", "clinton", "hillary clinton", "donald trump", "corona", "virus", "coronavirus"]
    else:
        track = track.split(",")
    stream.filter(track=track,
                  is_async=False)
    return "stream done"


# get the current user details and tweets
@stream.route('/myuser', methods=['GET', 'POST'])
def my_user():
    # creating object of TwitterClient Class
    try:
        user = api.me()
        retweets = api.retweets_of_me()
        user_timeline = api.user_timeline()
        home_timeline = api.home_timeline()
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

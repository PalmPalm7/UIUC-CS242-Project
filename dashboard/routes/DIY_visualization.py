import json

from flask import current_app, Blueprint, render_template, request
from textblob import TextBlob
from tweepy import OAuthHandler

from ..models.base import db
from ..models import User, Tweet, TwitterClient, StreamListener
from datetime import datetime
from datetime import timedelta
import tweepy
from sqlalchemy import desc, asc
from ..config import Config

DIY_visualization = Blueprint('DIY_visualization', __name__, url_prefix='/')
api = TwitterClient()


# return the DIY_visualization and returns the graph
@DIY_visualization.route('/DIY_visualization', methods=['GET', 'POST'])
def index():
    data ={}
    # if post request
    if request.method == "POST":
        print(request.form)
        type = request.form.get("type") # get the type
        file = request.files['file'] # get the file
        data = json.load(file)
        if type =="bar":
            data['type'] = "bar"
        elif type =="circle":
            data['type'] = "pie" # pie as we are using Chart js
        else:
            data['type'] = "line"

        data = json.dumps(data) # send to html for graph generation
        print(data)
    else:
        # if get method then read a sample data and return graph
        with current_app.open_resource('static/data/bar.json') as f:
            data = f.read().decode("utf-8")

    return render_template('DIY_visualization.html',jsondata=data)

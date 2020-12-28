import json

import click
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

cli = Blueprint('cli', __name__, url_prefix='/')
api = TwitterClient()


@cli.cli.command('start_stream')
@click.argument('tracks', required=False)
def start_stream(tracks):
    click.echo("cli start stream:" + str(tracks))
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.api.auth, listener=stream_listener)
    track = tracks
    click.echo("tracks", track)
    if track is None or len(track) < 2:
        track = ["trump", "donald trump", "corona", "virus", "coronavirus"]
    else:
        track = track.split(",")
    stream.filter(track=track,
                  is_async=False)
    click.echo("stream done")
    return "stream done"


@cli.cli.command('my_profile')
def profile():
    click.echo("cli my profile:")
    user = api.me()
    click.echo("======================USER==============================")
    click.echo(user)
    retweets = api.retweets_of_me()
    click.echo("=======================RETWEETS=============================")
    click.echo(retweets)

    user_timeline = api.user_timeline()
    click.echo("==========================USER TIMELINE==========================")
    click.echo(user_timeline)
    home_timeline = api.home_timeline(count=10)
    click.echo("===========================HOME TIMELINE=========================")
    click.echo(home_timeline)
    click.echo("profile done")
    return "profile done"

import json

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from .base import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=True)
    screen_name = db.Column(db.String(120), nullable=True)
    followers_count = db.Column(db.Integer, nullable=True)
    friends_count = db.Column(db.Integer, nullable=True)
    listed_count = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    time = db.Column(db.DateTime, nullable=True,default=datetime.utcnow)
    profile_image_url = db.Column(db.String(320), nullable=True)
    def to_json(self):
        return dict(id=self.id,
                    name=self.name,
                    time=self.time,
                    followers_count = self.followers_count,
                    profile_image_url=self.profile_image_url),

    def save(self):
        db.session.add(self)
        db.session.commit()


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    def __repr__(self):
        return {'id':self.id, 'name':self.name,'screen_name':self.screen_name,
                'follower':self.followers_count,
                'friends':self.friends_count,
                'listed':self.listed_count}

    def __str__(self):
        return 'User(id='+str(self.id)+', name='+str(self.name)+', screen_name='+str(self.screen_name)+ ')'

    def rollback(self):
        db.session.rollback()

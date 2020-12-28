import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .users import User
from .base import db

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(440), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    time = db.Column(db.DateTime, nullable=True,default=datetime.utcnow)
    retweet = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    sentiment_polarity = db.Column(db.Integer, nullable=True,default=0)
    sentiment_subjectivity = db.Column(db.Integer, nullable=True,default=0)
    user = db.relationship(User, backref='user')

    def to_json(self):
        return dict(id=self.id,
                    text=self.text,
                    time=self.time,
                    retweet = self.retweet,
                    user_id=self.user_id),

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def rollback(self):
        db.session.rollback()
    
    def __repr__(self):
        return {'id':self.id, 'text':self.text,'time':self.time,'user':self.user_id}

    def __str__(self):
        return 'Tweet(id='+str(self.id)+', text='+str(self.text)+', time='+str(self.text)+', user='+str(self.user_id)+ ')'
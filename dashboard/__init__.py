import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from . import models, routes
from .models.base import db, migrate

from .config import Config


def create_app():
    app = Flask(__name__, static_url_path='/dashboard/static')
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    models.init_app(app)
    routes.init_app(app)
    return app

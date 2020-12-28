import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    '''
    consumer_key = 'mpJnkTtXTRZABAeVXOchbXHsK'
    consumer_secret = 'zoRqmGb55QwHRDpWStbfXRppbcUirc0vS9gUT0NBU1Fz0EO7JK'
    access_token = '1251859884720742406-7KNfeb8RdNE1ww6s87lJXLDHTC5Qlg'
    access_token_secret = 'QI8EKgbAYDp0ErXeidkVaNa8Pus7HE7DY4de8UNoH9Fts'
    '''
    consumer_key = 'zPrl2oeXRExEO72Hmfp7uJuc7'
    consumer_secret = 'BMUtDjZmahuf9gGlC98fqAvwzGBeJOdpTXl1KfLAsAYn1MVQbA'
    access_token = '729953713960456192-dqn9JrP4AjuzcBWTkIBaWBTdS9AuEte'
    access_token_secret = 'bfAPSmFaWKmb6Dqj4qb618hySerhQoiaEuFOJgJSjcVJA'

    DEBUG = True
    USE_EMAIL = False
    DOMAIN_NAME = 'localhost:5000'
    SQLALCHEMY_ECHO = False
    PROD      = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
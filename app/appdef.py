import logging
import os

from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

from flask import Flask, current_app, request
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO=True

app = Flask(__name__)
config = Config()
app.config.from_object(config)
db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)

# json encoding


if not os.path.exists('.logs'):
    os.mkdir('.logs')
file_handler = RotatingFileHandler('.logs/api.log',
                                   maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)



import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sslify = SSLify(app)
db = SQLAlchemy(app)

import bot.views.index

import bot.models.user

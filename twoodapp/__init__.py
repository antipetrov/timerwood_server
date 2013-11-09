# coding: utf-8
__author__ = 'petrmatuhov'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# load config
import settings

# init app
app = Flask(__name__)
app.config.from_object(settings)

# start db
db = SQLAlchemy(app)

import views
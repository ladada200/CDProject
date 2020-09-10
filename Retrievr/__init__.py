# -*- coding: utf-8 -*-

# from . import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

Retrievr = Flask(__name__)
Retrievr.config.from_object('Retrievr.config.Config')
Retrievr.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(Retrievr)

from . import classes
from . import models
from . import routes


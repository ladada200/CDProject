# -*- coding: utf-8 -*-

# from . import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

CDProject = Flask(__name__)

from . import classes
from . import models
from . import routes

CDProject.config.from_object('CDProject.config.Config')
CDProject.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
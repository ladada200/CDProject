# -*- coding: utf-8 -*-

# from . import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

db = SQLAlchemy()

def create_app():
    Retrievr = Flask(__name__)
    Retrievr.config.from_object('Retrievr.config.Config')
    Retrievr.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(Retrievr)

    Bootstrap(Retrievr)

    with Retrievr.app_context():
        from . import classes
        from . import models
        from . import routes

        db.create_all()

    return Retrievr

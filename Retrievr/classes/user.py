# -*- coding: utf-8 -*-

from flask import session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime
from .basemodel import BaseMixin, Encryption
from hashlib import sha256
from dateutil.relativedelta import relativedelta
from . import app
import Retrievr

db = SQLAlchemy()

class UserObj(object):
    """User Object"""
    _login = None
    _password = None
    _active = False
    _accepted_invite = None
    _email = None

    def __init__(self,
                 login=None,
                 password=None,
                 email=None):
        """Initiates the User Object"""
        
        args = [login, password, email]

        try:
            for e in args:
                if e in [None, False, ""]:
                    raise Exception("Could not add user to Database, Stopping")

        
            self._login = login
            self._password = password
            self._email = email

            # send email proceedurel may not be necessary for personal use;

            return dict(
                login=self._login,
                password=self._password,
                email=self._email,
                accepted_invite=app.config.get('PERSONAL','ACCEPT_INVITE')
            )

        except Exception as e:
            app.logger.warn("%s, stopping" % e)
            return "%s" % e


# db.Model
class User(BaseMixin, db.Model):
    """Users table"""

    __tablename__ = "auth_users"
    __table_args__ = {'schema': "private" }
    _log_access = False

    uuid = db.Column(UUID(as_uuid=True), 
                     primary_key=True,
                     default=uuid4(),
                     unique=True,
                     nullable=False)

    login = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)     # this string will be encrypted elsewhere
    lastactive = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
    active = db.Column(db.Boolean, default=False)
    accepted_invite = db.Column(db.Boolean, default=False)
    email = db.Column(db.String, nullable=False, unique=True)

    def __init__(self,
                 login=None,
                 password=None,
                 lastactive=None,
                 active=False,
                 accepted_invite=False,
                 email=False):
        """User Class"""
        self.login = login
        self.password = password
        self.lastactive = lastactive
        self.active = active
        self.accepted_invite = accepted_invite
        self.email = email

    def __repr__(self):
        return '<User {}>'.format(self.login)

class LoginMethod(BaseMixin, Encryption):
    """Used for logging in"""

    def __init__(self,
                 login=None,
                 password=None,
                 **kwargs):
        """Initializes the class"""

        user = User.query.filter_by(login=login,
                                    active=True).first()

        if user:
            if self.decrypt(user.password) == password:
                session['context'] = dict(
                    uid="%s" % user.uuid,
                    online=True
                )
                session['expires'] = (datetime.now() + relativedelta()).strftime("%c")
                user.write(vals=dict(lastactive=datetime.now()), uuid=user.uuid)

        return None
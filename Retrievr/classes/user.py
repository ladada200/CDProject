# -*- coding: utf-8 -*-

from Retrievr import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime

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
                 email=None)
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
                email=self._email
                accepted_invite=app.config.get('PERSONAL','ACCEPT_INVITE')
            )

        except Exception as e:
            return "%s" % e


class User(db.Model):
    """Users table"""

    __tablename__ = "user"

    uuid = db.Column(UUID(as_uuid=True), 
                     primary_key=True,
                     default=uuid4(),
                     unique=True,
                     nullable=False)

    login = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)     # this string will be encrypted elsewhere
    lastactive = db.Column(db.Date, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
    active = db.Column(db.Boolean, default=False)
    accepted_invite = db.Column(db.Boolean, default=False)
    create_date = db.Column(db.Date, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
    write_date = db.Column(db.Date, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
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
        

    @classmethod
    def create(cls, vals, **kw):
        """Create user method"""
        obj = cls(vals)
        obj.session.add(obj)
        obj.session.commit()
    
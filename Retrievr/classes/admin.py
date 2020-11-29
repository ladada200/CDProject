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


class AdminSection(object):
    """Administrator section; has access to other methods / classes when necessary"""
    
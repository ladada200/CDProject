# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, Integer, ForeignKey
from uuid import uuid4

db = SQLAlchemy()

class Album(db.Model):
    """Artist table"""

    __tablename__ = "album"
    __table_args__ = {'schema': "public" }

    uuid = db.Column(UUID(as_uuid=True), 
                     primary_key=True,
                     default=uuid4(),
                     unique=True,
                     nullable=False)
    active = db.Column(db.Boolean, default=True)
    name = db.Column(db.String, nullable=False)

    # will include more columns later.

    def __init__(self):
        """Song table"""
        return 0

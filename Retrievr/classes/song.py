# -*- coding: utf-8 -*-

from Retrievr import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class Song(db.Model):
    """Song table"""

    __tablename__ = "song"

    uuid = db.Column(UUID(as_uuid=True), 
                     primary_key=True,
                     default=uuid4(),
                     unique=True,
                     nullable=False)
    active = db.Column(db.Boolean, default=True)
    name = db.Column(db.String, nullable=False)
    # artist = db.Column(UUID(as_uuid=True), ForeignKey('artist.uuid'))     # coming after artists

    # will include more columns later.

    def __init__(self):
        """Song table"""
        return 0

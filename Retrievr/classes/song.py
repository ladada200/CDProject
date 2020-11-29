# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from Retrievr.classes.artist import Artist
from Retrievr.classes.album import Album

db = SQLAlchemy()

class Song(db.Model):
    """Song table"""

    __tablename__ = "song"
    __table_args__ = {'schema': "public" }

    uuid = db.Column(UUID(as_uuid=True), 
                     primary_key=True,
                     default=uuid4(),
                     unique=True,
                     nullable=False)
    # active = db.Column(db.Boolean, default=True)
    name = db.Column(db.String, nullable=False)
    artist = db.Column(UUID(as_uuid=True), ForeignKey(Artist.uuid))     # coming after artists
    album = db.Column(UUID(as_uuid=True), ForeignKey(Album.uuid))
    length = db.Column(db.Integer, nullable=False)
    favorites = db.Column(db.Integer, nullable=False, default=0)
    release_date = db.Column(db.Date, nullable=True)

    artist_name = relationship(Artist, foreign_keys="Song.artist")
    album_name = relationship(Album, foreign_keys="Song.album")

    # will include more columns later.

    def __init__(self):
        """Song table"""
        return 0

    def __iter__(self):
        return {
            'name': self.name
        }

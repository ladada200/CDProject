# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, request, session, make_response
from CDProject import CDProject
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from base64 import b64encode

@CDProject.route('/song/', methods=['GET'])
@CDProject.route('/song/<song>', methods=['GET', 'POST'])
def index(song=None):
    """Does something"""

    if request.method == "GET":
        if song:
            return make_response(
                dict(
                    hello="World"
                ),
                200,
                {"Content-Type": "application/json"}
            )

        if not song:
            return make_response(
                dict(
                    user=dict(
                        curr_song=dict(
                            song_id=1,
                            song_uuid="%s" % uuid4(),
                            song_pos="%s" % timedelta(20)
                        )
                    ),
                    user_library=dict(
                        playlists=[],   # has songs
                        artists=[],     # has albums
                        albums=[],      # has songs
                        songs=[],       # all songs in library
                    ),
                    song=dict(
                        id=1,
                        uuid="%s" % uuid4(),
                        song_name="One week",
                        song_length="%s" % timedelta(seconds=174),
                        song_artist="Bare Naked Ladies",
                        song_album="One Week",
                        song_score=3.5,
                        song_fav=True,
                        created_uid=1,
                        created_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
                        write_uid=1,
                        write_date=datetime.strptime("2020-01-01", "%Y-%m-%d")
                    ),
                    artist=dict(
                        id=1,
                        uuid="%s" % uuid4(),
                        artist_name="Bare Naked Ladies",
                        artist_albums=[
                            dict(
                                album_id=1,
                                album_uuid="%s" % uuid4()
                            )
                        ],
                        album_count=1,  # computed
                        created_uid=1,
                        created_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
                        write_uid=1,
                        write_date=datetime.strptime("2020-01-01", "%Y-%m-%d")
                    ),
                    album=dict(
                        id=1,
                        uuid="%s" % uuid4(),
                        album_length="%s" % timedelta(seconds=3077),
                        album_artist="Bare Naked Ladies",
                        album_name="Stunt",
                        album_release=datetime.strptime("1999-04-20", "%Y-%m-%d"),
                        created_uid=1,
                        created_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
                        write_uid=1,
                        write_date=datetime.strptime("2020-01-01", "%Y-%m-%d")
                    ),
                    playlist=dict(
                        id=1,
                        uuid="%s" % uuid4(),
                        playlist_name="One week - playlist",
                        songs=[
                            dict(
                                id=1,
                                song_name="One week"
                            )
                        ],
                        created_uid=1,
                        created_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
                        write_uid=1,
                        write_date=datetime.strptime("2020-01-01", "%Y-%m-%d")
                    )
                ),
                200,
                {"Content-Type": "application/json"}
            )


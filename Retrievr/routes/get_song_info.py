# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, request, session, make_response, app
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from base64 import b64encode

song = Blueprint('song', __name__)

@song.route('/song/', methods=['GET'])
@song.route('/song/<song>', methods=['GET', 'POST'])
def index(song=None):
    """Does something"""

    artist_id = uuid4()
    album_id = uuid4()
    song_id = uuid4()
    playlist_id = uuid4()

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
                            song_uuid="%s" % song_id,
                            song_pos="%s" % timedelta(seconds=20)
                        )
                    ),
                    user_library=dict(
                        playlists=[playlist_id],   # has songs
                        artists=[artist_id],     # has albums
                        albums=[album_id],      # has songs
                        songs=[song_id],       # all songs in library
                    ),
                    songs=[
                        dict(
                            id=1,
                            uuid="%s" % song_id,
                            song_name="One week",
                            song_length="%s" % timedelta(seconds=174),
                            # song_artist="Bare Naked Ladies",    # many2one
                            # song_album="One Week",              # many2one
                            song_artists=[artist_id],             # many2many
                            song_album_uuid=album_id,
                            song_score=3.5,
                            song_fav=True,
                            created_uid=1,
                            created_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
                            write_uid=1,
                            write_date=datetime.strptime("2020-01-01", "%Y-%m-%d")
                        )   
                    ],
                    artists=[
                        dict(
                            id=1,
                            uuid="%s" % artist_id,
                            artist_name="Bare Naked Ladies", # many2one
                            artist_albums=[
                                dict(
                                    album_id=1,
                                    album_uuid="%s" % album_id
                                )
                            ],
                            album_count=1,  # computed
                            created_uid=1,
                            created_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
                            write_uid=1,
                            write_date=datetime.strptime("2020-01-01", "%Y-%m-%d")
                        )
                    ],
                    albums=[
                        dict(
                            id=1,
                            uuid="%s" % album_id,
                            album_length="%s" % timedelta(seconds=3077),
                            # album_artist="Bare Naked Ladies",   # many2many
                            album_artists=[artist_id],             # many2many
                            album_name="Stunt",
                            album_release=datetime.strptime("1999-04-20", "%Y-%m-%d"),
                            created_uid=1,
                            created_date=datetime.strptime("2020-01-01", "%Y-%m-%d"),
                            write_uid=1,
                            write_date=datetime.strptime("2020-01-01", "%Y-%m-%d")
                        )
                    ],
                    playlist=dict(
                        id=1,
                        uuid="%s" % playlist_id,
                        playlist_name="One week - playlist",
                        songs=[
                            dict(
                                id=1,
                                song_id=song_id,
                                song_pos="%s" % timedelta(seconds=20)
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


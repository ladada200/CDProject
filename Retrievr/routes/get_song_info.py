# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, request, session, make_response, app
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from base64 import b64encode

from . import app

from Retrievr.classes.song import Song
from Retrievr.classes.artist import Artist
from Retrievr.classes.album import Album

song = Blueprint('song', __name__)

def validate_uuid4(uuid_string):

    """
    Validate that a UUID string is in
    fact a valid uuid4.
    Happily, the uuid module does the actual
    checking for us.
    It is vital that the 'version' kwarg be passed
    to the UUID() call, otherwise any 32-character
    hex string is considered valid.
    """

    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        # If it's a value error, then the string 
        # is not a valid hex code for a UUID.
        return False

    # If the uuid_string is a valid hex code, 
    # but an invalid uuid4,
    # the UUID.__init__ will convert it to a 
    # valid uuid4. This is bad for validation purposes.

    return True

@song.route('/', methods=['GET'])
@song.route('/uuid/<song_uuid>', methods=['GET'])
@song.route('/name/<song_name>', methods=['GET'])
@song.route('/artist/<song_artist>', methods=['GET'])
@song.route('/album/<song_album>', methods=['GET'])
@song.route('/test/<test>', methods=['GET'])
def index(song_uuid=None, 
          song_name=None,
          song_artist=None,
          song_album=None,
          test=False):
    """Does something"""

    artist_id = uuid4()
    album_id = uuid4()
    song_id = uuid4()
    playlist_id = uuid4()

    if request.method == "GET":
        if song_uuid:
            if validate_uuid4(song_uuid):
                # check for song
                s_exec = Song.query.filter(Song.uuid == '%s' % song_uuid).one_or_none()
                # s_exec.dictfetchall()
                if s_exec:
                    return make_response(
                        dict(
                            response_time=datetime.now(),
                            response=[dict(
                                name=s_exec.name,
                                artist=s_exec.artist_name.name,
                                album=s_exec.album_name.name,
                                release_date=s_exec.release_date,
                                length=s_exec.length
                            )]
                        ),
                        200,
                        {"Content-Type": "application/json"}
                    )
                else:
                    return make_response(
                        dict(
                            error=dict(
                                code=404,
                                message="""No song found."""
                            ),
                        ), 
                        404, 
                        {"Content-Type": "application/json"}
                    )

            else:
                return make_response(
                    dict(
                        error=dict(
                            code=404,
                            message="""No song found."""
                        ),
                    ), 
                    404, 
                    {"Content-Type": "application/json"}
                )

        if song_name:
            s_exec = Song.query.filter(Song.name.ilike(f'%{song_name}%')).all()

            if s_exec:
                x = []
                for i in s_exec:
                    x.append(
                        dict(
                            name=i.name,
                            artist=i.artist_name.name,
                            album=i.album_name.name,
                            release_date=i.release_date,
                            length=i.length
                        )
                    )

                return make_response(
                    dict(
                        response_time=datetime.now(),
                        response=x
                    ),
                    200,
                    {"Content-Type": "application/json"}
                )
            else:
                return make_response(
                    dict(
                        error=dict(
                            code=404,
                            message="""No song found."""
                        ),
                    ), 
                    404, 
                    {"Content-Type": "application/json"}
                )

        if song_artist:
            s_exec = Song.query.join(Song.artist_name)\
                .filter(Artist.name.ilike(f'%{song_artist}%'), 
                        Artist.active == True).all()

            if s_exec:
                x = []
                for i in s_exec:
                    x.append(
                        dict(
                            name=i.name,
                            artist=i.artist_name.name,
                            album=i.album_name.name,
                            release_date=i.release_date,
                            length=i.length
                        )
                    )

                return make_response(
                    dict(
                        response_time=datetime.now(),
                        response=x
                    ),
                    200,
                    {"Content-Type": "application/json"}
                )
            else:
                return make_response(
                    dict(
                        error=dict(
                            code=404,
                            message="""No song found."""
                        ),
                    ), 
                    404, 
                    {"Content-Type": "application/json"}
                )

        if song_album:
            s_exec = Song.query.join(Song.album_name)\
                .filter(Album.name.ilike(f'%{song_album}%'), 
                        Album.active == True).all()

            if s_exec:
                x = []
                for i in s_exec:
                    x.append(
                        dict(
                            name=i.name,
                            artist=i.artist_name.name,
                            album=i.album_name.name,
                            release_date=i.release_date,
                            length=i.length
                        )
                    )

                return make_response(
                    dict(
                        response_time=datetime.now(),
                        response=x
                    ),
                    200,
                    {"Content-Type": "application/json"}
                )
            else:
                return make_response(
                    dict(
                        error=dict(
                            code=404,
                            message="""No song found."""
                        ),
                    ), 
                    404, 
                    {"Content-Type": "application/json"}
                )

        if test:
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


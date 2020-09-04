# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

import configparser
import codecs

working_dir = "%s/CDProject/config" % os.getcwd()
config = configparser.ConfigParser(inline_comment_prefixes='#')
config.read(("%s/local.cfg" % working_dir) if os.path.isfile('%s/local.cfg' % working_dir) else ("%s/template.cfg" % working_dir), encoding="utf-8")


class Config(object):
    # Debug
    DEBUG = config.get('DEBUG', 'DEBUG')
    CSRF_ENABLED = True

    # Host
    HOST_PORT=config.get('HOST', 'host_port')
    HOST_HTTPS=config.get('HOST', 'host_https')
    HOST_NAME=config.get('HOST', 'host_name')
    HOST_FS=config.get('HOST', 'host_FS')
    HOST_RDP_PORT=config.get('HOST', 'host_rdp_port')

    # DB
    SQLALCHEMY_DATABASE_URI="postgresql:///%s:%s@%s:%s/%s" % (config.get('DB', 'db_username'),
                                                              config.get('DB', 'db_password'),
                                                              config.get('DB', 'db_host'),
                                                              config.get('DB', 'db_port'),
                                                              config.get('DB', 'db_name'))

    # Song info
    SONG_STORE=config.get('SONG_FORMAT', 'song_store')
    SONG_DISPLAY_FORMAT=config.get('SONG_FORMAT', 'song_display_format')
    SONG_RATING=config.get('SONG_FORMAT', 'song_rating')
    SONG_TAGS=config.get('SONG_FORMAT', 'song_tags')

    # admin
    ADMIN_USER=config.get('ADMIN', 'admin_user')
    ADMIN_PASS=config.get('ADMIN', 'admin_pass')

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
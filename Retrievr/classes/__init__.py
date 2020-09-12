# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)
app.config.from_object('Retrievr.config.Config')

from . import user
from . import artist
from . import album
from . import song
from . import song_info
from . import socket_handler
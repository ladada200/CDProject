# -*- coding: utf-8 -*-
    from flask import Flask
    from logging.handlers import TimedRotatingFileHandler
    import os
    from datetime import datetime
    import logging

    app = Flask(__name__)
    app.config.from_object('Retrievr.config.Config')

    LOG_PATH = os.path.join(os.getcwd(), "%s" % app.config.get('LOG_PATH'))

    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    handler = TimedRotatingFileHandler('%s/Retrievr-%s.log' % (LOG_PATH,
                                                            datetime.now().strftime("%Y-%m-%d")),
                                    when='midnight',
                                    backupCount=30)
    handler.setLevel(logging.DEBUG if app.config.get('DEBUG') else logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    app.logger.setLevel(logging.DEBUG if app.config.get('DEBUG') else logging.INFO)
    app.logger.addHandler(handler)

from . import user
from . import artist
from . import album
from . import song
from . import song_info
from . import socket_handler
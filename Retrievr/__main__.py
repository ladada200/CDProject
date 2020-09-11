# -*- coding: utf-8 -*-

from . import current_app as Retrievr

if __name__ == '__main__':
    Retrievr.run(host=Retrievr.config['HOST_NAME'], port=Retrievr.config['HOST_PORT'], debug=Retrievr.config['DEBUG'])
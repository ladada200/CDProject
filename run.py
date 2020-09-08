# -*- coding: utf-8 -*-

from CDProject import CDProject

# app.register_blueprint(CDProject.routes)

# db = SQLAlchemy(app)

if __name__ == '__main__':
    CDProject.run(host=CDProject.config['HOST_NAME'], port=CDProject.config['HOST_PORT'], debug=CDProject.config['DEBUG'])
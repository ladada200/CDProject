# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, request, session, make_response
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.dialects.postgresql import JSON
# from flask import render_template
# from .. import db

from CDProject import CDProject

@CDProject.route('/', methods=['GET'])
def index():
    """Does something"""

    return make_response(
        {'test': 'worked'},
        200,
        {"Content-Type": "application/json"}
    )


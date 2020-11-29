# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, render_template, abort, url_for, redirect, request, session, make_response
from jinja2 import TemplateNotFound

from . import app
from Retrievr import classes
from Retrievr.classes import user

main = Blueprint('main', __name__, template_folder="templates")

@main.route("/", methods=['GET'])
def show_main():
    try:
        u_name = user.User.query.filter_by(uuid=session.get('context', {}).get('uid')).first()

        context = dict(
            u_name=u_name.login if u_name else None
        )

        if request.method == 'GET':
            return make_response(render_template("/index.html", u_name=context.get('u_name')))
    except TemplateNotFound:
        return redirect(url_for('main.show_main'))


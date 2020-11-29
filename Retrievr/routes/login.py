# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, render_template, abort, url_for, redirect, request, session, make_response
from jinja2 import TemplateNotFound

from . import app
from Retrievr import classes

login_form = Blueprint('login_form', __name__, template_folder="templates")

@login_form.route('/logout/', endpoint="logout", methods=['GET'])
def do_logout():
    try:
        user = classes.user.LoginMethod()
        user.logout_method()
        return redirect(url_for('main.show_main'))
    except TemplateNotFound:
        return redirect(url_for('login_form.index'))

@login_form.route('/login/', endpoint="login", methods=['POST', 'GET'])
def do_login():
    try:
        if request.method == 'GET':
            if session.get('context', {}).get('uid', None):
                return redirect(url_for('main.show_main'))
            # this section is reserved for what to do once the user has a session;
            # we should default whatever this behaviour is to the same as teh response from the connection
            # as outlined below on authentication.

            return redirect(url_for('login_form.index'))
        elif request.method == 'POST':
            # add logic here to check against users table for authentication;
            # add session token with context once completed.

            # let's start down that path.
            response = redirect(url_for('main.show_main'))
            data = request.form.to_dict()
            user = classes.user.LoginMethod(login=data.get('login'),
                                            password=data.get('password'),
                                            method=data.get('auth_method'))

            if not user.login_method():
                app.logger.debug("SESSION OUTPUT: %s" % session)
                # response.set_cookie('retrievr', b'test')
                # app.logger.debug("REQ %s" % request.cookies.get('retrievr'))
                response = make_response(render_template('auth/index.html', error="Could not login."))

            return response
    except TemplateNotFound:
        return redirect(url_for('login_form.index'))

@login_form.route("/", endpoint="index", methods=['GET'])
def index():
    try:
        return make_response(render_template("auth/index.html"))
    except TemplateNotFound:
        return redirect(url_for('login_form.index'))
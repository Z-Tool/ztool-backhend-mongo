#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jack003.com
from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth
from ..models import User, AnonymousUser
from . import api_1_0
from .errors import unauthorized
from .constant import login_required_list

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.objects.filter(email=email_or_token)
    if not user:
        return False
    user = user.first_or_404()
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api_1_0.before_app_request
@auth.login_required
def before_request():
    if request.method != 'OPTIONS':
        if g.current_user.is_anonymous and request.endpoint:
            if '.' in request.endpoint and request.endpoint.startswith('api_1_0') and request.endpoint.split('.')[1] in login_required_list:
                return unauthorized('Unauthorized account')
    else:
        pass


@api_1_0.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify(token=g.current_user.generate_auth_token(expiration=86400), expiration=86400, email=g.current_user.email)


@api_1_0.route('/test')
@auth.login_required
def login_test():
    if g.current_user == AnonymousUser():
        return jsonify(status='error', data='Anonymous user!'), 401
    else:
        return jsonify(email=g.current_user.email, status='success')

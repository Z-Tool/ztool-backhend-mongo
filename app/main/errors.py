#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jack003.com
from flask import jsonify
from . import main


@main.app_errorhandler(400)
def bad_request(e):
    return jsonify({'error': '403 bad request'}), 400


@main.app_errorhandler(401)
def unauthorized(e):
    return jsonify({'error': '401 unauthorized'}), 401


@main.app_errorhandler(403)
def forbidden(e):
    return jsonify({'error': '403 forbidden'}), 403


@main.app_errorhandler(404)
def page_not_found(e):
    return jsonify({'error': '404 page not found'}), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': '500 internal server error'}), 500

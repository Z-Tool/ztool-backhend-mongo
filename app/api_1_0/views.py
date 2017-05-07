#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jarrekk.com
import datetime
import json
import socket
import time

import feedparser
import pythonwhois
import requests
from flask import jsonify, request, current_app

from . import api_1_0
from ..decorators import jsonp


@api_1_0.route('/', methods=['GET'])
def index():
    with open('app/api_1_0/APIList.json') as f:
        data = f.read()
    return jsonify(data=json.loads(data), status='success')


@api_1_0.route('/time', methods=['GET'])
@jsonp
def get_time():
    return jsonify(status='success', data=datetime.datetime.now())


@api_1_0.route('/rss', methods=['GET'])
@jsonp
def parse_rss():
    url = request.args.get('url', None)
    if url:
        feed = feedparser.parse(url)
        # todo remove \n
        return jsonify(status='success', data=json.loads(json.dumps(feed, default=lambda obj: time.strftime(
            '%Y-%m-%d %H:%M:%S', obj) if isinstance(obj, time.struct_time) else None)))
    else:
        return jsonify(status='error', data='needs url parameter'), 400


@api_1_0.route('/info')
@jsonp
def info():
    app = current_app._get_current_object()
    key = app.config['IP_INFO_DB_KEY']
    ip = request.args.get('ip', None)
    if not ip:
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr
        user_agent = {'browser': request.user_agent.browser,
                      'language': request.user_agent.language,
                      'platform': request.user_agent.platform,
                      'string': request.user_agent.string,
                      'version': request.user_agent.version,
                      'status': 'success',
                      'message': 'localhost user agent information'}
    else:
        user_agent = {'status': 'error',
                      'message': 'not query localhost information'}
    ip_info = requests.get('http://api.ipinfodb.com/v3/ip-city/?key={0}&ip={1}&format=json'.format(key, ip)).json()
    return jsonify(status='success', data={'ip': ip, 'ip_information': ip_info, 'user_agent': user_agent}), 200 if \
    ip_info['statusCode'] != 'ERROR' else jsonify(status='error'), 400


@api_1_0.route('/whois')
@jsonp
def whois():
    dom = request.args.get('domain', None)
    if dom:
        detail = pythonwhois.get_whois(dom)
        return jsonify(status='success', data=detail)
    else:
        return jsonify(status='error', data='needs domain parameter'), 400


@api_1_0.route('/nslookup')
@jsonp
def nslookup():
    dom = request.args.get('domain', None)
    if dom:
        try:
            result = socket.gethostbyname(dom)
        except:
            result = 'domain error, check your input'
        if result.startswith('domain'):
            ip_info = None
        else:
            app = current_app._get_current_object()
            key = app.config['IP_INFO_DB_KEY']
            ip_info = requests.get(
                'http://api.ipinfodb.com/v3/ip-city/?key={0}&ip={1}&format=json'.format(key, result)).json()
        return jsonify(status='success', data={'DNS record': result, 'IP infomation': ip_info})
    else:
        return jsonify(status='error', data='needs domain parameter'), 400

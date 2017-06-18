#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 18/6/17
# email: me@jarrekk.com
import requests
from flask import jsonify
from . import api_1_0


@api_1_0.route('/hn/<sub_url>', methods=['GET'])
def hacker_news(sub_url):
    sub_url = '/'.join(sub_url.split('.')) + '.json'
    # print('https://hacker-news.firebaseio.com/' + sub_url)
    try:
        r = requests.get('https://hacker-news.firebaseio.com/' + sub_url)
    except:
        return jsonify(status='error', data='request error')
    else:
        return jsonify(status='success', data=r.json())

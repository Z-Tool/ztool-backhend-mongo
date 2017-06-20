#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 18/6/17
# email: me@jarrekk.com
import html
import requests
from flask import jsonify
from app.tasks import test_add
from . import api_1_0


@api_1_0.route('/hn/<sub_url>', methods=['GET'])
def hacker_news(sub_url):
    sub_url = '/'.join(sub_url.split('.')) + '.json'
    # print('https://hacker-news.firebaseio.com/' + sub_url)
    try:
        r = requests.get('https://hacker-news.firebaseio.com/' + sub_url)
    except:
        return jsonify(status='error', data={'message': 'request error'}), 400
    else:
        if 'item' in sub_url:
            if r.json().get('text', None):
                data = r.json()
                data['text'] = html.unescape(data['text'])
                return jsonify(status='success', data=data)
        return jsonify(status='success', data=r.json())


@api_1_0.route('/hn/list/<items>', methods=['GET'])
def get_list(items):
    try:
        items = eval(items)
    except:
        return jsonify(status='error', data={'message': 'items error'}), 400
    # items = items.split(',')
    print(items)
    data = []
    for item in items:
        try:
            r = requests.get('https://hacker-news.firebaseio.com/v0/item/' + str(item) + '.json')
        except Exception as e:
            print(e)
            return jsonify(status='error', data={'message': 'request error'}), 400
        else:
            result = r.json()
            if result.get('text', None):
                result['text'] = html.unescape(result['text'])
            data.append(result)
    return jsonify(status='success', data=data)


@api_1_0.route('/testc')
def testc():
    test_add.delay(1, 2)
    return 'add ok'

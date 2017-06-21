#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 6/21/17
# email: me@jack003.com
import html
import requests


def get_list(stype):
    url = 'https://hacker-news.firebaseio.com/v0/' + stype + 'stories.json'
    r = requests.get(url)
    return r.json()


def get_content(clist=[]):
    data = []
    for item in clist:
        try:
            r = requests.get('https://hacker-news.firebaseio.com/v0/item/' + str(item) + '.json')
        except Exception as e:
            print(e)
            return None
        else:
            result = r.json()
            if result.get('text', None):
                result['text'] = html.unescape(result['text'])
            data.append(result)
    return data

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jarrekk.com
from flask import jsonify

from . import main


@main.route('/', methods=['GET'])
def hello_world():
    return jsonify(status='success', message='welcome to jarrekk!')

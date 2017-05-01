#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jarrekk.com
from flask import jsonify
from . import api_1_0
from ..decorators import jsonp
from ..models import Jalpc_pv_count


@api_1_0.route('/jalpc/pv_count', methods=['GET'])
@jsonp
def jalpc_count():
    cnt = Jalpc_pv_count.access()
    return jsonify(status='success', data=cnt)

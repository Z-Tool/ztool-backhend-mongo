#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jack003.com
from functools import wraps
from flask import request, current_app


def jsonp(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', None)
        rtn = f(*args, **kwargs)
        if isinstance(rtn, tuple):
            content = '{0}({1})'.format(str(callback), rtn[0].data) if callback else rtn[0].data
            status = rtn[1]
        else:
            content = '{0}({1})'.format(str(callback), rtn.data) if callback else rtn.data
            status = 200
        return current_app.response_class(content, mimetype='application/json', status=status)

    return decorated_function

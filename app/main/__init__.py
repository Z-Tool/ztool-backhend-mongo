#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jack003.com
"""
main blueprint
"""
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jack003.com
"""
some API for Jalpc & personal usage
"""
from flask import Blueprint

api_1_0 = Blueprint('api_1_0', __name__)

# from . import views, jalpc, authentication
from . import jalpc

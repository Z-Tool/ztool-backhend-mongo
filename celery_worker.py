#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 20/06/2017
# email: me@jack003.com
import os
from app import create_app, celery

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()

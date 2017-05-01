#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jarrekk.com
from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

from config import config

db = MongoEngine()
login_manager = LoginManager()
login_manager.session_protection = 'strong'


def create_app(config_name):
    app = Flask(__name__)
    # CORS(app, supports_credentials=False, resources={r"/api/*": {"origins": "*"}})
    CORS(app, supports_credentials=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as index_blueprint
    app.register_blueprint(index_blueprint, url_prefix='/')

    from .api_1_0 import api_1_0 as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app

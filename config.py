#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jarrekk.com
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jack vps on vultr'
    IP_INFO_DB_KEY = os.environ.get('IPINFODBKEY') or 'key'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'jalpc',
        'host': '127.0.0.1',
        'port': 27017
    }
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    import logging
    logging.getLogger('flask_cors').level = logging.DEBUG


class TestConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'jalpc',
        'host': '127.0.0.1',
        'port': 27017
    }
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    import logging
    logging.getLogger('flask_cors').level = logging.DEBUG


class ProdConfig(Config):
    DEBUG = False
    # DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'jalpc',
        # 'host': '127.0.0.1',
        'host': 'mongo',
        'port': 27017
    }
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
    import logging
    logging.getLogger('flask_cors').level = logging.DEBUG


config = {
    'default': DevConfig,
    'testing': TestConfig,
    'prod': ProdConfig
}

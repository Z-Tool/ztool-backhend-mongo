#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jarrekk.com
import os

from flask_script import Manager, Shell

from app import create_app, db
from app.models import Jalpc_pv_count, User

if os.environ.get('FLASK_CONFIG') == 'prod':
    from gevent import monkey

    monkey.patch_all()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, Jalpc=Jalpc_pv_count, User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

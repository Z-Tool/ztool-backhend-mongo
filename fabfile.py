#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jack003.com
from __future__ import unicode_literals
import os

from fabric.api import run, roles, cd
from fabric.context_managers import env
from fabric.contrib.project import rsync_project

code_dir = '/jalpc'
local_dir = '/Users/jack/Dropbox/Jack/jalpc-flask'
exclude = ('.DS_Store', '*pyc', '.git', '.idea', '*sqlite3', 'migrations')

env.roledefs = {
    'vps': ['root@vps.jack003.com']
}


@roles('vps')
def install():
    run('apt-get update && apt-get install -y python-pip python-dev uwsgi-plugin-python nginx')
    rsync_project(local_dir='requirements.txt', remote_dir=code_dir)
    with cd(code_dir):
        run('pip2.7 install -r requirements.txt')
        run('mv jalpc.conf /etc/nginx/sites-enabled/ && rm -f /etc/nginx/sites-enabled/default && service nginx reload')
        run('mkdir /home/www && chown -R www-data. /home/www')
        run('/usr/bin/uwsgi jalpc.ini')


@roles('vps')
def pip():
    rsync_project(local_dir='requirements.txt', remote_dir=code_dir)
    with cd(code_dir):
        run('pip2.7 install -r requirements.txt')


@roles('vps')
def deploy():
    rsync_project(local_dir='.', remote_dir=code_dir, exclude=exclude)
    run('cp -a /jalpc/app/static /jalpc/static && source ~/.jalpc-env && uwsgi --reload /run/uwsgi.pid')


@roles('vps')
def backup():
    rsync_project(local_dir=local_dir, remote_dir=os.path.join(code_dir, 'migrations/versions'), upload=False, exclude=exclude)


@roles('vps')
def upload():
    rsync_project(local_dir=os.path.join(local_dir, 'versions'), remote_dir=os.path.join(code_dir, 'migrations'), exclude=exclude)

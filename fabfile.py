#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 05/02/17
# email: me@jarrekk.com
from fabric.api import run, roles, cd, local
from fabric.context_managers import env
from fabric.contrib.project import rsync_project

code_dir = '/backhend'
exclude = (
    '.DS_Store',
    '*pyc',
    '.git',
    '.idea',
    '*sqlite3',
    'migrations',
    'node_modules',
    'readme_files',
    '__pycache__',
    '.travis'
)

env.roledefs = {
    'vps': ['root@vps.jarrekk.com']
}


@roles('vps')
def rebuild(container=''):
    rsync_project(local_dir='.', remote_dir=code_dir, exclude=exclude)
    with cd(code_dir):
        if container:
            run('docker-compose down {0}; docker-compose build {1}'.format(container, container))
        else:
            run('docker-compose down; docker-compose build')


@roles('vps')
def up(container=''):
    with cd(code_dir):
        if container:
            run('docker-compose up -d {0}'.format(container))
        else:
            run('docker-compose up -d')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 05/02/17
# email: me@jarrekk.com
from fabric.api import run, roles, cd, local
from fabric.context_managers import env
from fabric.contrib.project import rsync_project

code_dir = '/backhend'
exclude = ('.DS_Store', '*pyc', '.git', '.idea', '*sqlite3', 'migrations', 'node_modules', 'readme_files', '__pycache__')

env.roledefs = {
    'vps': ['root@vps.jarrekk.com']
}

crontabs = """# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command
0 0 * * * /bin/bash /root/dropbox_uploader.sh delete mongodb
5 0 * * * /bin/bash /root/dropbox_uploader.sh upload /data/mongodb /
"""


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


@roles('vps')
def crontab():
    run('echo "{0}" > /tmp/cron && crontab /tmp/cron && rm -f /tmp/cron'.format(crontabs))

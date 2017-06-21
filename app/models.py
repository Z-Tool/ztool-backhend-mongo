#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jarrekk.com
from datetime import datetime
from bson import ObjectId

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login_manager


class BaseDocument(db.Document):
    created_at = db.DateTimeField(verbose_name='create_time', required=True)
    updated_at = db.DateTimeField(verbose_name='update_time', required=True)
    meta = {'abstract': True}

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(BaseDocument, self).save(*args, **kwargs)


class Jalpc_pv_count(BaseDocument):
    count = db.IntField(verbose_name='pv_count', required=True)

    @staticmethod
    def init_db(count=1):
        s = Jalpc_pv_count(count=count)
        s.save()
        return s

    @staticmethod
    def access():
        if Jalpc_pv_count.objects.all():
            s = Jalpc_pv_count.objects.all()[0]
            s.count += 1
            s.save()
            return s.count
        else:
            s = Jalpc_pv_count.init_db(295500)
            return s.count


class Hacker_news_cache(BaseDocument):
    stype = db.StringField(verbose_name='cache_type', required=True)
    data_list = db.ListField(verbose_name='data_list', required=True)
    data_content = db.ListField(verbose_name='data_content', required=True)


class User(UserMixin, BaseDocument):
    email = db.EmailField(verbose_name='email', required=True)
    username = db.StringField(verbose_name='username', required=True)
    password_hash = db.StringField(verbose_name='password', required=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': str(self.id)})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.objects.get_or_404(id=ObjectId(data['id']))

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        pass

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.objects.get_or_404(id=ObjectId(user_id))

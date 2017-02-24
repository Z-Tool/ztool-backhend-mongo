#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 2/23/17
# email: me@jack003.com
from datetime import datetime

from flask import url_for, current_app
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login_manager


class BaseDocument(db.Document):
    created_at = db.DateTimeField(verbose_name=u'create_time', required=True)
    updated_at = db.DateTimeField(verbose_name=u'update_time', required=True)
    meta = {'abstract': True}

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(BaseDocument, self).save(*args, **kwargs)


class JalpcPVCount(BaseDocument):
    count = db.IntField(verbose_name=u'pv_count', required=True)

    @staticmethod
    def init_db(count=1):
        s = JalpcPVCount(count=count)
        db.session.add(s)
        db.session.commit()
        return s

    @staticmethod
    def access():
        if JalpcPVCount.query.count():
            s = JalpcPVCount.query.first()
            s.count += 1
            db.session.add(s)
            db.session.commit()
            return s.count
        else:
            s = JalpcPVCount.init_db(195000)
            return s.count


class User(UserMixin, BaseDocument):
    email = db.EmailField(verbose_name=u'email', required=True)
    username = db.StringField(verbose_name=u'username', required=True)
    password_hash = db.StringField(verbose_name=u'password', required=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts': url_for('api.get_user_posts', id=self.id, _external=True),
            'followed_posts': url_for('api.get_user_followed_posts',
                                      id=self.id, _external=True),
            'post_count': self.posts.count()
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        pass

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 6/28/17
# email: me@jack003.com
import json
import os
import unittest

from app import create_app


# from app.models import User


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(os.getenv('FLASK_CONFIG') or 'default')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertTrue('welcome' in response.get_data(as_text=True))

    def test_jalpc(self):
        response = self.client.get('/api/v1.0/jalpc/pv_count')
        self.assertEqual(response.status_code, 200)

    def test_ip_info(self):
        response = self.client.get('/api/v1.0/info?ip=8.8.8.8')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['status'], 'success')
        self.assertEqual(json_response['data']['ip_information']['cityName'], 'Mountain View')

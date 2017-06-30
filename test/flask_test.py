#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Kun Jia
# date: 6/28/17
# email: me@jack003.com
import json
import os
import sys
import unittest

TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.realpath(os.path.join(TESTS_ROOT, '..')))

from app import create_app


# from app.models import User


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(os.getenv('FLASK_CONFIG') or 'testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    '''index page'''
    def test_home_page(self):
        response = self.client.get('/')
        self.assertTrue('welcome' in response.get_data(as_text=True))

    '''api index page'''
    def test_api_home_page(self):
        response = self.client.get('/api/v1.0')
        self.assertTrue(response.status_code in [200, 301])

    '''api time'''
    def test_time(self):
        response = self.client.get('/api/v1.0/time')
        self.assertEqual(response.status_code, 200)

    '''api whois'''
    def test_whois(self):
        response = self.client.get('/api/v1.0/whois?domain=jarrekk.com')
        self.assertEqual(response.status_code, 200)

    def test_whois_fail(self):
        response = self.client.get('/api/v1.0/whois')
        self.assertEqual(response.status_code, 400)

    '''api info'''
    def test_ip_info(self):
        response = self.client.get('/api/v1.0/info?ip=8.8.8.8')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['status'], 'success')
        self.assertEqual(json_response['data']['ip_information']['cityName'], 'Mountain View')

    def test_ip_info_self(self):
        response = self.client.get('/api/v1.0/info')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['status'], 'success')
        self.assertEqual(json_response['data']['user_agent']['status'], 'success')

    '''api nslookup'''
    def test_nslookup(self):
        response = self.client.get('/api/v1.0/nslookup?domain=vps.jarrekk.com')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(json_response['status'], 'success')

    def test_nslookup_fail_none(self):
        response = self.client.get('/api/v1.0/nslookup')
        self.assertEqual(response.status_code, 400)

    def test_nslookup_fail_invalid(self):
        response = self.client.get('/api/v1.0/nslookup?domain=abcdefg')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['status'], 'success')
        self.assertEqual(json_response['data']['DNS record'], 'domain error, check your input')

    '''api pkg'''
    def test_pkg(self):
        response = self.client.get('/api/v1.0/pypi/imgkit.svg')
        self.assertEqual(response.status_code, 200)

    '''api jalpc'''
    def test_jalpc(self):
        response = self.client.get('/api/v1.0/jalpc/pv_count')
        self.assertEqual(response.status_code, 200)

    def test_hack_news(self):
        from app.tasks import cache_data
        self.assertTrue(cache_data())
        response = self.client.get('/api/v1.0/hn/cache/top')
        self.assertEqual(response.status_code, 200)
        slist = json.loads(response.data.decode('utf-8'))['data']['slist']
        response = self.client.get('/api/v1.0/hn/list/' + str(slist))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/api/v1.0/hn/v0.item.160705')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()

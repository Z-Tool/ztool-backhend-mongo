#!/usr/bin/env bash

fab rebuild:flask && fab up:flask
fab rebuild:celery && fab up:celery

#FROM python:2.7.13-wheezy
FROM ubuntu:16.04

MAINTAINER Jarrekk me@jarrekk.com

ADD ./requirements.txt /tmp/requirements.txt
ADD ./jalpc-docker.ini /tmp/jalpc-docker.ini

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    git \
    python \
    python-dev \
    python-setuptools \
    python-pip \
    uwsgi-plugin-python && \
    pip install -U pip setuptools && \
    rm -rf /var/lib/apt/lists/*
RUN pip install -r /tmp/requirements.txt
CMD uwsgi /tmp/jalpc-docker.ini

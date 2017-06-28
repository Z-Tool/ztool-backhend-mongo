FROM python:3.6.1

MAINTAINER Jarrekk me@jarrekk.com

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    git \
    apt-utils && \
    pip install -U pip setuptools && \
    rm -rf /var/lib/apt/lists/*

ADD ./jalpc-docker.ini /tmp/jalpc-docker.ini
ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
WORKDIR /jalpc
CMD uwsgi /tmp/jalpc-docker.ini

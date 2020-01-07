FROM python:3.8.1-slim-buster

MAINTAINER Lukasz Admin

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app/ /app

RUN useradd user
USER user

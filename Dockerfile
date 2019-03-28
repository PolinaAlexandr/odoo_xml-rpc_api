FROM python:3.6.8-alpine

WORKDIR app

RUN pip install pika

COPY . .

FROM python:3.5
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt install -y python3-dev python-psycopg2 libjpeg-dev libpq-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip install -r requirements/local.txt

FROM python:latest
RUN apt-get update
RUN apt-get install -y pkg-config libsystemd-dev gcc

RUN pip install paho-mqtt systemd-python pymongo cysystemd

RUN apt-get -y install libpq-dev
RUN pip install psycopg2 pydantic

COPY ../.. /mpp-solar/
RUN pip install -e /mpp-solar/
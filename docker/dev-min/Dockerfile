FROM python:3.9-buster
RUN apt-get update
RUN apt-get install -y pkg-config libsystemd-dev gcc
RUN pip install cysystemd

RUN pip install pyserial paho-mqtt PyYAML

# RUN apt-get -y install libpq-dev
# RUN pip install psycopg2

COPY ./ /mpp-solar/

RUN pip install -e /mpp-solar/
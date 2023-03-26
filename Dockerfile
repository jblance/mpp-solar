FROM python:3.10.4-slim-bullseye
RUN apt update
RUN apt-get install -y pkg-config libsystemd-dev gcc
RUN pip install paho-mqtt systemd-python pymongo

RUN apt-get -y install libpq-dev
RUN pip install psycopg2

ARG CACHEBUST=1
ADD . /mpp-solar/
RUN pip install -e /mpp-solar/

CMD ["sleep", "3600"]

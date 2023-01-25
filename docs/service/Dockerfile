FROM python:3.10.4-slim-bullseye
RUN apt update
RUN apt-get install -y pkg-config libsystemd-dev gcc

RUN pip install paho-mqtt systemd-python mppsolar

WORKDIR "/etc/mpp-solar"

CMD mpp-solar -C mpp-solar.conf --daemon

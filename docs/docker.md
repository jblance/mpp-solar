# Run mpp-solar using Docker

__created / tested by [Rob Wolff](https://github.com/robwolff3)__

1. Download the [Dockerfile here](https://github.com/jblance/mpp-solar/blob/master/docs/service/Dockerfile) or copy and paste below to the Docker server you want to run the mpp-solar container on:
```
FROM python:3.10.4-slim-bullseye
RUN apt update
RUN apt-get install -y pkg-config libsystemd-dev gcc
RUN pip install paho-mqtt systemd-python mppsolar
WORKDIR "/etc/mpp-solar"
CMD mpp-solar -C mpp-solar.conf --daemon
```

2. In the same folder as the Dockerfile run `docker build -t mpp-solar .` to build the container.

3. Create a config file called `mpp-solar.conf` where the rest of your docker config files are stored. Reference the mpp-solar config file [documentation here](https://github.com/jblance/mpp-solar/blob/master/docs/configfile.md) or see mine as an example below:
```
[SETUP]
pause=1
mqtt_broker=MQTTHOST
mqtt_user=MQTTPASS
mqtt_pass=MQTTUSER

[LVX6048WP]
port=/dev/ttyUSB0
protocol=PI17
command=GS#PS
tag=mpp
outputs=hass_mqtt
```

4. Run the container using Docker command:
```
$ docker run -d --name=mpp-solar \
    --restart unless-stopped \
    -v ${CONFIGDIR}/mpp-solar:/etc/mpp-solar \
    --device /dev/ttyUSB0:/dev/ttyUSB0 \
    --privileged \
    mpp-solar
```
   Or run the container using Docker Compose:
```
version: '3'
services:
 mpp-solar:
   image: mpp-solar
   container_name: mpp-solar
   privileged: true
   restart: unless-stopped
   volumes:
     - ${CONFIGDIR}/mpp-solar:/etc/mpp-solar
   devices:
     - /dev/ttyUSB0:/dev/ttyUSB0
```

# MPP Solar Inverter Python Package

## Note refactor underway - code likely broken / changing
use the 'stable' release [0.4.6](https://github.com/jblance/mpp-solar/releases/tag/v0.4.6)

_Note: python2 no longer supported_

[![Build Status](https://travis-ci.org/jblance/mpp-solar.svg?branch=master)](https://travis-ci.org/jblance/mpp-solar)
[![Coverage Status](https://coveralls.io/repos/github/jblance/mpp-solar/badge.svg?branch=master)](https://coveralls.io/github/jblance/mpp-solar?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/08c51e13554d4f77836c6cc7b010df2c)](https://www.codacy.com/app/jblance/mpp-solar?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jblance/mpp-solar&amp;utm_campaign=Badge_Grade)

Python package with reference library of serial commands (and responses)
for MPP and similar inverters, some known to work (to varying amounts):
- PIP-4048MS
- IPS-4000WM
- Voltronic Axpert MKS 5KVA Off-grid Inverter-Chargers
- LV5048

Good overview and technical discussion here
http://forums.aeva.asn.au/viewtopic.php?f=31&t=4332

## Tested On
- Raspberry Pi 3
- 2x USB to serial adapters (like https://www.adafruit.com/product/18)
- connected to 2x PIP-4048MS inverters connected in parallel

Also
- Raspberry Pi 3
- USB cable to USB port of inverter
- connected to 1x PIP-4048MS (/dev/hidraw0 on Pi)

Also
- Raspberry Pi
- 3x USB to serial adapters
- connected to 3x LV5048 inverters

Also
- Ubuntu 2020.04
- Direct USB connection to Inverter (LV5048)
- see [documented approach](docs/ubuntu_install.md)

## Install
`sudo python3 ./setup.py install`

[Documented Ubuntu Install](docs/ubuntu_install.md)

## MQTT / Influx / Grafana Setup ##
Instruction of one way of connecting the inverter output to Grafana
[Setup Instructions](docs/MQTT_Influx_Grafana.md)

## Example Usage
[Usage](docs/usage.md)

## Protocol / Command Documentation
[Protocol Index](docs/README.md)

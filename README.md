# MPP-Solar Device Python Package #

__Note: python less than v3.6 not supported__


Python package with reference library of serial commands (and responses)
designed to get information from inverters and other solar and power devices
Support for:
- MPP-Solar and similar inverters, e.g.
  - PIP-4048MS
  - IPS-4000WM
  - Voltronic Axpert MKS 5KVA Off-grid Inverter-Chargers
  - LV5048
- JK BMS
  - JK-B2A24S (HW version 3.0)
  - JK-B1A24S (HW version 3.0)




Good overview and technical discussion here of mpp-solar inverters: http://forums.aeva.asn.au/viewtopic.php?f=31&t=4332

## Tested On ##
- Raspberry Pi 3
  - 2x USB to serial adapters (like https://www.adafruit.com/product/18)
  - connected to 2x PIP-4048MS inverters connected in parallel

- Raspberry Pi 3
  - USB cable to USB port of inverter
  - connected to 1x PIP-4048MS (/dev/hidraw0 on Pi)

- Raspberry Pi
  - 3x USB to serial adapters
  - connected to 3x LV5048 inverters

- Ubuntu 2020.04
  - Direct USB connection to Inverter (LV5048)
  - see [documented approach](docs/ubuntu_install.md)

## Install latest stable version ##
`sudo pip install mpp-solar`

## venv Install - recommended if testing new features / release ##
for when you want to keep the install and dependencies separate from the rest of the environment
* create venv folder `mkdir ~/venv`
* create venv `python3 -m venv ~/venv/mppsolar`
    * might need python3-venv installed
* activate venv `source venv/mppsolar/bin/activate` (needed each time before using)
* pip install from git `pip install -e "git+https://github.com/jblance/mpp-solar.git#egg=mpp-solar"` (only needed if the code is updated)

see worked example [here](docs/venv.md)

## Install development version from github ##
`sudo pip install -e "git+https://github.com/jblance/mpp-solar.git#egg=mpp-solar"`

## Install (from source)
* Download or clone the repo
* From the directory that has the requirements files:
    * `sudo pip install -r requirements.txt`  # for the minimal install (dependances must be installed manually)
    * `sudo pip install -r requirements-serial.txt`  # for the mqtt install (includes pyserial)
    * `sudo pip install -r requirements-full.txt`  # for the full install (includes pyserial, mqtt and bluepy)
__Note:__ need `sudo apt-get install libglib2.0-dev` for bluepy

[Documented Ubuntu Install](docs/ubuntu_install.md)

## Using a config file
* You can setup a config file instead of using command line options
* this is particularly useful for running as a service / dameon
[details here](docs/configfile.md)

## Troubleshooting ##
 [Troubleshooting](docs/troubleshooting.md)

## MQTT / Influx / Grafana Setup ##
Instruction of one way of connecting the inverter output to Grafana
[Setup Instructions](docs/MQTT_Influx_Grafana.md)

## Example Usage
`$ mpp-solar -p /dev/hidraw0 -c QPI`

`$ jkbms -p 3C:A5:09:0A:AA:AA -c getInfo`
[More detailed usage](docs/usage.md)

## Protocol / Command Documentation
[Protocol Index](docs/README.md)
[Interface](docs/interface.md)

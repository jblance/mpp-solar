# MPP-Solar Device Python Package #

__Note: python earlier than version 3.6 is not supported__


Python package with reference library of commands (and responses)
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
- Victron VE Direct Devices:
 - tested on SmartShunt 500A


## Compute hardware support ##
The python code is designed to run on Linux type python environments using python 3.6 or newer


## Installation ##

### latest stable version ###
`sudo pip install mpp-solar`

### venv Install - recommended if testing new features / release ###
for when you want to keep the install and dependencies separate from the rest of the environment
* create venv folder `mkdir ~/venv`
* create venv `python3 -m venv ~/venv/mppsolar`
    * might need python3-venv installed
* activate venv `source venv/mppsolar/bin/activate` (needed each time before using)
* pip install from git `pip install -e "git+https://github.com/jblance/mpp-solar.git#egg=mpp-solar"` (only needed if the code is updated)

see worked example [here](docs/venv.md)

### Install development version from github ###
`sudo pip install -e "git+https://github.com/jblance/mpp-solar.git#egg=mpp-solar"`

### Ubuntu Install example ###
[Documented Ubuntu Install](docs/ubuntu_install.md)


## Usage ###
* Run 'QPI' command against an inverter (will use default protocol PI30) connected via direct USB on /dev/hidraw0 (will output results to screen)
  * `$ mpp-solar -p /dev/hidraw0 -c QPI`
* Run the above with more information about what is happening (INFO level messages)
  * `$ mpp-solar -p /dev/hidraw0 -c QPI -I`
* Run the above with LOTS of information about what is happening (DEBUG level messages)
  * `$ mpp-solar -p /dev/hidraw0 -c QPI -D`
* Run the top but output to mqtt
  * `$ mpp-solar -p /dev/hidraw0 -c QPI -o mqtt -q mqttbroker`
* Show help / usage
  * `$ mpp-solar -h`
* List commands fir protocol PI41
  * `$ mpp-solar -P PI41 -c`
* List output modules available
  * `$ mpp-solar -o`

* Run 'getInfo' command against jkbms BMS with bluetooth MAC '3C:A5:09:0A:AA:AA'
  * `$ jkbms -p 3C:A5:09:0A:AA:AA -c getInfo`

[More detailed usage](docs/usage.md)

[More documentation](docs/README.md)

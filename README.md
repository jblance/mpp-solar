# MPP-Solar Device Python Package #

__Note: python earlier than version 3.6 is not supported__


Python package with reference library of commands (and responses)
designed to get information from inverters and other solar inverters and power devices

Currently has support for:
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
- Daly BMS (coming soon)

## Compute hardware support ##
The python code is designed to run on Linux type python environments using python 3.6 or newer
[hardware that has been known to work](docs/hardware.md)

## Installation ##
* to get the latest stable version: `sudo pip install mpp-solar`
* [more installation options](docs/installation.md)

## Usage ###
`$ mpp-solar -h` or `$ jkbms -h` will display the available options

[More detailed usage](docs/usage.md)

[More detailed documentation](docs/README.md)

## Troubleshooting ##
[Troubleshooting](docs/troubleshooting.md)

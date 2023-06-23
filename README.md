# MPP-Solar Device Python Package #

__BREAKING CHANGES__
- minimum python supported 3.10 for version >=0.16.0
- command separator changed to `#`


Python package with reference library of commands (and responses)
designed to get information from inverters and other solar inverters and power devices

Currently has support for:
- MPP-Solar and similar inverters, e.g.
  - PIP-4048MS
  - IPS-4000WM
  - Voltronic Axpert MKS 5KVA Off-grid Inverter-Chargers
  - LV5048
- JK BMS
- Victron VE Direct Devices:
  - tested on SmartShunt 500A
- Daly BMS

## Install ##
- `pip install mppsolar` (minimal install), or
- `pip install mppsolar[ble]` (install including BLE support aka jkbms), or
- `docker pull jblance/mppsolar:latest` (docker install)


## Documentation ##
[See the wiki for documentation](https://github.com/jblance/mpp-solar/wiki)

## Support ##
If you want to tip me for this work, you can now buy me a coffee

[![buymeacoffee1](https://user-images.githubusercontent.com/1266998/225745276-54d6a4d4-a1ed-44f9-a1f2-e99eb1aa2812.png)](https://www.buymeacoffee.com/jblance)


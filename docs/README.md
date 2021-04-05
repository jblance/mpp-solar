# Documentation #

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


## Using a config file
* You can setup a config file instead of using command line options
* this is particularly useful for running as a service / dameon
[details here](docs/configfile.md)

## Troubleshooting ##
 [Troubleshooting](docs/troubleshooting.md)

## MQTT / Influx / Grafana Setup ##
Instruction of one way of connecting the inverter output to Grafana
[Setup Instructions](docs/MQTT_Influx_Grafana.md)


## Protocol / Command Documentation
[Protocol Index](docs/README.md)
[Interface](docs/interface.md)


## Protocol / Command References ##

File | Comment | Source
--- | --- | ---
[PI00_RS232_Protocol.pdf](PI00_RS232_Protocol.pdf) | | [link](https://www.photovoltaikforum.com/core/attachment/7135-protocol-pdf/)
[PI16_VoltronicPowerSUNNYProtocol.md](PI16_VoltronicPowerSUNNYProtocol.md) | |
[PI17_InfiniSolar-5KW-protocol-20160309.pdf](PI17_InfiniSolar-5KW-protocol-20160309.pdf) | |
[PI18_InfiniSolar-V-protocol-20170926.pdf](PI18_InfiniSolar-V-protocol-20170926.pdf) | |
[PI30_Communication-Protocol-20150924-Customer.pdf](PI30_Communication-Protocol-20150924-Customer.pdf) | |
[PI30_HS_MS_MSX_RS232_Protocol_20140822_after_current_upgrade.pdf](PI30_HS_MS_MSX_RS232_Protocol_20140822_after_current_upgrade.pdf) | | [link](http://forums.aeva.asn.au/uploads/293/HS_MS_MSX_RS232_Protocol_20140822_after_current_upgrade.pdf)
[PI30_PIP-GK_MK-Protocol.pdf](PI30_PIP-GK_MK-Protocol.pdf) | |
[PI34_ForumEA_B_mppt-1.pdf)](PI34_ForumEA_B_mppt-1.pdf) | |
[PI41_LV5048.5KW.protocol-20190222.for.customer.pdf](PI41_LV5048.5KW.protocol-20190222.for.customer.pdf) | |
[VE.Direct-Protocol-3.29.pdf](VE.Direct-Protocol-3.29.pdf) | Protocol description for Victron VE Direct devices | [link](https://www.victronenergy.com/support-and-downloads/whitepapers)
[BMV-7xx-HEX-Protocol-public.pdf](BMV-7xx-HEX-Protocol-public.pdf) | HEX Protocol description for Victron VE Direct devices  | [link](https://www.victronenergy.com/support-and-downloads/whitepapers)

## Other documentation ##

* [Inverter to Grafana via MQTT, Telegraf and InfluxDB](MQTT_Influx_Grafana.md)
* [Ubuntu Install](ubuntu_install.md)
* [Troubleshooting](troubleshooting.md)

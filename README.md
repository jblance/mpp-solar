# MPP Solar Inverter Python Package

[![Build Status](https://travis-ci.org/jblance/mpp-solar.svg?branch=master)](https://travis-ci.org/jblance/mpp-solar)
[![Coverage Status](https://coveralls.io/repos/github/jblance/mpp-solar/badge.svg?branch=master)](https://coveralls.io/github/jblance/mpp-solar?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/08c51e13554d4f77836c6cc7b010df2c)](https://www.codacy.com/app/jblance/mpp-solar?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jblance/mpp-solar&amp;utm_campaign=Badge_Grade)

Python package with reference library of serial commands (and responses) 
for PIP-4048MS inverters - aka:
- PIP-4048MS 
- IPS-4000WM 
- Voltronic Axpert MKS 5KVA Off-grid Inverter-Chargers

Good overview and technical discussion here
http://forums.aeva.asn.au/viewtopic.php?f=31&t=4332

## Tested On
- a Raspberry Pi 3
- using 2x USB to serial adapters (like https://www.adafruit.com/product/18)
- to connect to 2x PIP-4048MS inverters connected in parallel

## Install
`python ./setup.py install`

## Usage
`$ mpp-solar -h`
```
usage: mpp-solar-script.py [-h] [-c COMMAND]
                           [-ll {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                           [-d DEVICE] [-b BAUD] [-l] [-s] [-t] [-R]

MPP Solar Command Utility

optional arguments:
  -h, --help            show this help message and exit
  -c COMMAND, --command COMMAND
                        Command to run
  -ll {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level
  -d DEVICE, --device DEVICE
                        Serial device to communicate with
  -b BAUD, --baud BAUD  Baud rate for serial communications
  -l, --listknown       List known commands
  -s, --getStatus       Get Inverter Status
  -t, --getSettings     Get Inverter Settings
  -R, --showraw         Display the raw results
```

## Available Commands
`$ mpp-solar -l`
```
-------- List of known commands --------
PBT: Set Battery Type
PSDV: Set Battery Cut-off Voltage
Q1: Q1 query
QBOOT: DSP Has Bootstrap inquiry
QDI: Device Default Settings inquiry
QFLAG: Device Flag Status inquiry
QID: Device Serial Number inquiry
QMCHGCR: Max Charging Current Options inquiry
QMUCHGCR: Max Utility Charging Current Options inquiry
QOPM: Output Mode inquiry
QPGSn: Parallel Information inquiry
QPI: Device Protocol ID inquiry
QPIGS: Device General Status Parameters inquiry
QPIRI: Device Current Settings inquiry
QPIWS: Device warning status inquiry
QVFW: Main CPU firmware version inquiry
QVFW2: Secondary CPU firmware version inquiry
```

## Example
`$ mpp-solar -s`
```
================ Status ==================
Parameter                       Value           Unit
ac_input_frequency              00.0            Hz
ac_input_voltage                000.0           V
ac_output_active_power          0152            W
ac_output_apparent_power        0207            VA
ac_output_frequency             50.0            Hz
ac_output_load                  004             %
ac_output_voltage               230.2           V
allowscconflag                  01
battery_capacity                100             %
battery_charging_current        018             A
battery_discharge_current       00000           A
battery_temperature             046             Deg_C
battery_voltage                 57.40           V
battery_voltage_from_scc        57.45           V
bus_voltage                     459             V
chargeaveragecurrent            00
fan_lock_status                 Not locked
fan_pwm_speed                   0030            Percent
inverter_charge_status          bulk stage
inverter_heat_sink_temperature  0057            Deg_C
inverter_temperature            034             Deg_C
pv_input_current_for_battery    0021            A
pv_input_voltage                069.9           V
scc_charge_power                1258            W
scc_flag                        SCC is powered and communicating
scc_pwm_temperature             051             Deg_C
sync_frequency                  50.00
transformer_temperature         057             Deg_C
```

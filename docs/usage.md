# Usage (PI30)

- The commands default to using `/dev/ttyUSB0` if you are using direct USB connection try adding `-d /dev/hidraw0` to the commands
- if you have other USB devices connected the inverter might show up as `/dev/hidraw1` or `/dev/hidraw2`
- if uncertain, remove and re-connect the connection to the inverter and look at the end of the `dmesg` response to see what was reconnected
- also in some instances only root has access to the device that the inverter is connected to - if you are getting no response try using `sudo`
  - if you want to be able to use a hidraw device as pi (or other users)
  - create a file `/etc/udev/rules.d/99-hidraw.rules` with the below as the content
    ```
    KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0660", GROUP="plugdev"
    ```
    - after a restart (or replug of the USB cable) any user of the plugdev group will be able to read from/write to any /dev/hidraw device
- if you are getting no/unexpected results add `-D` to the command to get a heap of extra information

`$ mpp-solar -h`
```
usage: mpp-solar [-h] [-c COMMAND] [-D] [-I] [-d DEVICE] [-b BAUD] [-M MODEL]
                 [-l] [-s] [-t] [-R] [-p]

MPP Solar Command Utility

optional arguments:
  -h, --help            show this help message and exit
  -c COMMAND, --command COMMAND
                        Command to run
  -D, --enableDebug     Enable Debug and above (i.e. all) messages
  -I, --enableInfo      Enable Info and above level messages
  -d DEVICE, --device DEVICE
                        Serial (or USB) device to communicate with, defaults
                        to /dev/ttyUSB0
  -b BAUD, --baud BAUD  Baud rate for serial communications, defaults to 2400
  -M MODEL, --model MODEL
                        Specifies the inverter model to select commands for,
                        defaults to "standard", currently supports LV5048
  -l, --listknown       List known commands
  -s, --getStatus       Get Inverter Status
  -t, --getSettings     Get Inverter Settings
  -R, --showraw         Display the raw results
  -p, --printcrc        Display the command and crc and nothing else

```

## Available Commands
`$ mpp-solar -l` or `$ mpp-solar -l -M LV5048`
```
F
Set Device Output Frequency
-- examples: F50 (set output frequency to 50Hz) or F60 (set output frequency to 60Hz)

MCHGC
Set Max Charging Current (for parallel units)
-- examples: MCHGC040 (set unit 0 to max charging current of 40A), MCHGC160 (set unit 1 to max charging current of 60A)

MNCHGC
Set Utility Max Charging Current (more than 100A) (for 4000/5000)
-- example: MNCHGC1120 (set unit 1 utility max charging current to 120A)

MUCHGC
Set Utility Max Charging Current
-- example: MUCHGC130 (set unit 1 utility max charging current to 30A)

PBCV
Set Battery re-charge voltage
-- example PBCV44.0 - set re-charge voltage to 44V (12V unit: 11V/11.3V/11.5V/11.8V/12V/12.3V/12.5V/12.8V, 24V unit: 22V/22.5V/23V/23.5V/24V/24.5V/25V/25.5V, 48V unit: 44V/45V/46V/47V/48V/49V/50V/51V)

PBDV
Set Battery re-discharge voltage
-- example PBDV48.0 - set re-discharge voltage to 48V (12V unit: 00.0V/12V/12.3V/12.5V/12.8V/13V/13.3V/13.5V/13.8V/14V/14.3V/14.5, 24V unit: 00.0V/24V/24.5V/25V/25.5V/26V/26.5V/27V/27.5V/28V/28.5V/29V, 48V unit: 00.0V/48V/49V/50V/51V/52V/53V/54V/55V/56V/57V/58V, 00.0V means battery is full(charging in float mode).)

PBFT
Set Battery Float Charging Voltage
-- example PBFT58.0 - set battery float charging voltage to 58V (48.0 - 58.4V for 48V unit)

PBT
Set Battery Type
-- examples: PBT00 (set battery as AGM), PBT01 (set battery as FLOODED), PBT02 (set battery as USER)

PCP
Set Device Charger Priority
-- examples: PCP00 (set utility first), PCP01 (set solar first), PCP02 (HS only: set solar and utility), PCP03 (set solar only charging)

PCVV
Set Battery C.V. (constant voltage) charging voltage
-- example PCVV48.0 - set charging voltage to 48V (48.0 - 58.4V for 48V unit)

PEPD
Set the enabled / disabled state of various Inverter settings (e.g. buzzer, overload, interrupt alarm)
-- examples: PEABJ/PDKUVXYZ (enable A buzzer, B overload bypass, J power saving / disable K LCD go to default after 1min, U overload restart, V overtemp restart, X backlight, Y alarm on primary source interrupt, Z fault code record)

PF
Set Control Parameters to Default Values
-- example PF (reset control parameters to defaults)

PGR
Set Grid Working Range
-- examples: PCR00 (set device working range to appliance), PCR01 (set device working range to UPS)

POP
Set Device Output Source Priority
-- examples: POP00 (set utility first), POP01 (set solar first), POP02 (set SBU priority)

POPM
Set Device Output Mode (for 4000/5000)
-- examples: POPM01 (set unit 0 to 1 - parallel output), POPM10 (set unit 1 to 0 - single machine output), POPM02 (set unit 0 to 2 - phase 1 of 3), POPM13 (set unit 1 to 3 - phase 2 of 3), POPM24 (set unit 2 to 4 - phase 3 of 3)

PPCP
Set Parallel Device Charger Priority (for 4000/5000)
-- examples: PPCP000 (set unit 1 to 00 - utility first), PPCP101 (set unit 1 to 01 - solar first), PPCP202 (set unit 2 to 02 - solar and utility), PPCP003 (set unit 0 to 03 - solar only charging)

PPVOKC
Set PV OK Condition
-- examples: PPVOKC0 (as long as one unit has connected PV, parallel system will consider PV OK), PPVOKC1 (only if all inverters have connected PV, parallel system will consider PV OK)

PSDV
Set Battery Cut-off Voltage
-- example PSDV40.0 - set battery cut-off voltage to 40V (40.0 - 48.0V for 48V unit)

PSPB
Set Solar Power Balance
-- examples: PSPB0 (PV input max current will be the max charged current), PSPB1 (PV input max power will be the sum of the max charge power and loads power)

Q1
Q1 query


QBOOT
DSP Has Bootstrap inquiry


QDI
Default Settings inquiry
-- queries the default settings from the Inverter

QFLAG
Flag Status inquiry
-- queries the enabled / disabled state of various Inverter settings (e.g. buzzer, overload, interrupt alarm)

QID
Device Serial Number inquiry
-- queries the device serial number

QMCHGCR
Max Charging Current Options inquiry
-- queries the maximum charging current setting of the Inverter

QMOD
Mode inquiry
-- queries the Inverter mode

QMUCHGCR
Max Utility Charging Current Options inquiry
-- queries the maximum utility charging current setting of the Inverter

QOPM
Output Mode inquiry
-- queries the output mode of the Inverter (e.g. single, parallel, phase 1 of 3 etc)

QP2GS
Parallel Information inquiry
-- example: QP2GS1 queries the values of various metrics from instance 1 of parallel setup Inverters (numbers from 0)

QPGS
Parallel Information inquiry LV5048
-- example: QPGS1 queries the values of various metrics from instance 1 of parallel setup Inverters (numbers from 0)

QPI
Protocol ID inquiry
-- queries the device protocol ID. e.g. 30 for HS series

QPIGS
General Status Parameters inquiry LV5048
-- queries the value of various metrics from the Inverter

QPIGS2
General Status Parameters inquiry
-- queries the value of various metrics from the Inverter

QPIRI
Current Settings inquiry for LV5048
-- queries the current settings from the Inverter

QPIWS
Warning status inquiry
-- queries any active warnings flags from the Inverter

QVFW
Main CPU firmware version inquiry
-- queries the main CPU firmware version

QVFW2
Secondary CPU firmware version inquiry
-- queries the secondary CPU firmware version
```

## Example
`$ mpp-solar -s`
```
================ Status ==================
Parameter                       Value           Unit
ac_input_frequency              00.0            Hz
ac_input_voltage                000.0           V
ac_output_active_power          0119            W
ac_output_apparent_power        0161            VA
ac_output_frequency             49.9            Hz
ac_output_load                  003             %
ac_output_voltage               230.0           V
allowscconflag                  01
battery_capacity                100             %
battery_charging_current        012             A
battery_discharge_current       00000           A
battery_temperature             053             Deg_C
battery_voltage                 57.50           V
battery_voltage_from_scc        57.45           V
bus_voltage                     460             V
chargeaveragecurrent            00
fan_lock_status                 Not locked
fan_pwm_speed                   0040            Percent
gpio13                          00
inverter_charge_status          float
inverter_heat_sink_temperature  0069            Deg_C
inverter_temperature            045             Deg_C
is_ac_charging_on               0               True - 1/False - 0
is_battery_voltage_to_steady_while_charging     0               True - 1/False - 0
is_charging_on                  1               True - 1/False - 0
is_configuration_changed        0               True - 1/False - 0
is_load_on                      1               True - 1/False - 0
is_sbu_priority_version_added   0               True - 1/False - 0
is_scc_charging_on              1               True - 1/False - 0
is_scc_firmware_updated         1               True - 1/False - 0
not_used                        000
parallel_warning??              0000
pv_input_current_for_battery    0014            A
pv_input_voltage                103.8           V
scc_charge_power                0580            W
scc_flag                        SCC is powered and communicating
scc_pwm_temperature             059             Deg_C
sync_frequency                  50.00
time_until_the_end_of_absorb_charging   00000           sec
time_until_the_end_of_float_charging    00000           sec
transformer_temperature         068             Deg_C
unknown_value_in_response       010
```

# Config File Specifications

```
[SETUP]
### NOTE WELL: No end of line comments are supported!
### Commented out lines must be at the beginning of a line but can be indented.

# Number of seconds to pause between loops of processing the sections
# i.e. the pause at the end of an entire run through the config file
# default is 60
pause=5

# ipaddress or hostname of the mqtt broker, default is 'localhost'
mqtt_broker=localhost

# mqtt broker port number, default is 1883
mqtt_port=1883

# username and password (if required) for mqtt broker, default to None and not used unless defined
mqtt_user=username
mqtt_pass=password

### The section name needs to be unique
### There can be multiple sections which are processed sequentially without pause
### The pause occurs after all sections are processed, before the next loop
### The name is used for:
###   client_id in MQTTIO (using in the command and response topics)

[SectionName]

# required - protocol to use to decode command and response (default: PI30)
protocol=PI30

# required - type of device (default: mppsolar)
type=mppsolar

# required - port used to communicate with device (default: /dev/ttyUSB0)
port=/dev/ttyUSB0

# optional - baud rate of port communications (default: 2400)
baud=2400

# required - hash separated list of commands to execute
command=QPI

# optional - used in various ways in the outputs (see output list)
tag=TagName

# required - comma separated list of outputs (default: screen)
outputs=screen

# optional - used to override the automatic port type determination
porttype=serial

# optional - if defined only field names that match the filter will be output (uses python re format)
filter=^voltage

# optional - if defined any field names that match the filter will be
exclfilter=test excluded from the output (uses python re format)

# optional - redefines UDP publish port (default: 5555)
udpport=5566
```

[list of outputs](usage.md#List-available-output-processors)

## Config file examples

### mpp-solar running on a Pi with 2x PIP4048
- that is connected (via a USB to serial adapter on /dev/ttyUSB0)
- to a two PIP4048 (protocol PI30) setup in parallel (with parallel cards)
- with an MQTT broker on 'mqtthost'

```
[SETUP]
pause=5
mqtt_broker=mqtthost

[Inverter_1]
port=/dev/ttyUSB0
protocol=PI30
command=QPGS0
tag=QPGS0
outputs=mqtt

[Inverter_2]
port=/dev/ttyUSB0
protocol=PI30
command=QPGS1
tag=QPGS1
outputs=mqtt
```

this would generate mqtt messages like:
```
...[snip]...
{'topic': 'QPGS0/status/fault_code/value', 'payload': 'No fault'}
{'topic': 'QPGS0/status/grid_voltage/value', 'payload': 0.0}
{'topic': 'QPGS0/status/grid_voltage/unit', 'payload': 'V'}
{'topic': 'QPGS0/status/grid_frequency/value', 'payload': 0.0}
{'topic': 'QPGS0/status/grid_frequency/unit', 'payload': 'Hz'}
{'topic': 'QPGS0/status/ac_output_voltage/value', 'payload': 230.6}
...[snip]...
{'topic': 'QPGS1/status/fault_code/value', 'payload': 'No fault'}
{'topic': 'QPGS1/status/grid_voltage/value', 'payload': 0.0}
{'topic': 'QPGS1/status/grid_voltage/unit', 'payload': 'V'}
{'topic': 'QPGS1/status/grid_frequency/value', 'payload': 0.0}
{'topic': 'QPGS1/status/grid_frequency/unit', 'payload': 'Hz'}
{'topic': 'QPGS1/status/ac_output_voltage/value', 'payload': 230.6}
...[snip]...
```

### mpp-solar running on a ubuntu with a single LV5048
- connected via a direct USB cable to the inverter (/dev/hidraw0)
```
# This example would work on a single LV5048
[LV5048]
protocol=PI41
port=/dev/hidraw0
command=QPGS0,QP2GS0
tag=Inverter1
outputs=influx2_mqtt
```
this would generate mqtt messages like:
```
...[snip]...
'topic': 'mpp-solar', 'payload': 'mpp-solar,command=Inverter1 l2_ac_output_frequency=59.98'}
{'topic': 'mpp-solar', 'payload': 'mpp-solar,command=Inverter1 l2_ac_output_apparent_power=149'}
{'topic': 'mpp-solar', 'payload': 'mpp-solar,command=Inverter1 l2_ac_output_active_power=130'}
{'topic': 'mpp-solar', 'payload': 'mpp-solar,command=Inverter1 l2_load_percentage=5'}
{'topic': 'mpp-solar', 'payload': 'mpp-solar,command=Inverter1 l2_battery_voltage=56.1'}
{'topic': 'mpp-solar', 'payload': 'mpp-solar,command=Inverter1 l2_battery_charging_current=0'}
...[snip]...
```

### jkbms running on pi using BLE to communicate with a JK-B2A24S

```
[JKBMS]
type=jkbms
protocol=JK04
port=3C:A5:49:AA:AA:AA
command=getCellData
tag=CellData
outputs=influx_mqtt
```
this would generate mqtt messages like:
```
...[snip]...
{'topic': 'jkbms', 'payload': 'CellData,setting=average_cell_voltage value=2.327305316925049,unit=V'}
{'topic': 'jkbms', 'payload': 'CellData,setting=delta_cell_voltage value=0.178879976272583,unit=V'}
{'topic': 'jkbms', 'payload': 'CellData,setting=highest_cell value=8,unit='}
{'topic': 'jkbms', 'payload': 'CellData,setting=lowest_cell value=12,unit='}
{'topic': 'jkbms', 'payload': 'CellData,setting=flags value=0101,unit='}
{'topic': 'jkbms', 'payload': 'CellData,setting=uptime value=0D3H23M12S,unit='}
...[snip]...
```

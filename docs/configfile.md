# Config File Specifications

```
[SETUP]
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

# The section name needs to be unique
# There can be multiple sections which are processed sequentially without pause
# The pause occurs after all sections are processed, before the next loop
# The name is used for:
#   client_id in MQTTIO (using in the command and response topics)
#
[SectionName]
#
protocol=PI30     # required - protocol to use to decode command and response (default: PI30)
type=mppsolar     # required - type of device (default: mppsolar)
port=/dev/ttyUSB0 # required - port used to communicate with device (default: /dev/ttyUSB0)
baud=2400         # optional - baud rate of port communications (default: 2400)
command=QPI       # required - comma separated list of commands to execute
tag=TagName       # optional - used in various ways in the outputs (see output list)
outputs=screen    # required - comma separated list of outputs (default: screen)
porttype=serial   # optional - used to override the automatic port type determination
filter=^voltage   # optional - if defined only field names that match the filter will be output (uses python re format)
excl_filter=test  # optional - if defined any field names that match the filter will be excluded from the output (uses python re format)
```

[list of outputs](usage.md#List-available-output-processors)

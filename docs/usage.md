# Usage

## Troubleshooting / Notes ##
- The commands default to using `/dev/ttyUSB0` if you are using direct USB connection try adding `-d /dev/hidraw0` to the commands
- if you have other USB devices connected the inverter might show up as `/dev/hidraw1` or `/dev/hidraw2`
- if uncertain, remove and re-connect the connection to the inverter and look at the end of the `dmesg` response to see what was reconnected
- also in some instances only root has access to the device that the inverter is connected to - if you are getting no response try using `sudo`
- if you are getting no/unexpected results add `-I` to the command to get some extra information
- if you are getting no/unexpected results add `-D` to the command to get lots of extra information

## mpp-solar arguments
`$ mpp-solar -h`
```
usage: mpp-solar [-h] [-n NAME] [-t TYPE] [-p PORT] [-d DEVICE]
                 [-P {PI00,PI16,PI18,PI30,PI41}] [-T TAG] [-b BAUD] [-M MODEL]
                 [-o OUTPUT] [-q MQTTBROKER] [-c COMMAND] [--listknown]
                 [--getstatus] [--getsettings] [--printcrc] [-R] [-v] [-D]
                 [-I]

MPP Solar Command Utility, version: 0.7.0, First refactor version - under
development

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Specifies the device name - used to differentiate
                        different devices
  -t TYPE, --type TYPE  Specifies the device type (default: mppsolar)
  -p PORT, --port PORT  Specifies the device communications port (/dev/ttyUSB0
                        [default], /dev/hidraw0, test, ...)
  -d DEVICE, --device DEVICE
                        DEPRECATED, use -p
  -P {PI00,PI16,PI18,PI30,PI41}, --protocol {PI00,PI16,PI18,PI30,PI41}
                        Specifies the device command and response protocol,
                        (default: PI30)
  -T TAG, --tag TAG     Override the command name and use this instead (for
                        mqtt and influx type output processors)
  -b BAUD, --baud BAUD  Baud rate for serial communications (default: 2400)
  -M MODEL, --model MODEL
                        Specifies the inverter model to select commands for,
                        defaults to "standard", currently supports LV5048
  -o OUTPUT, --output OUTPUT
                        Specifies the output processor(s) to use [comma
                        separated if multiple] (screen [default], influx_mqtt,
                        influx2_mqtt, mqtt, hass_config, hass_mqtt)
  -q MQTTBROKER, --mqttbroker MQTTBROKER
                        Specifies the mqtt broker to publish to if using a
                        mqtt output (localhost [default], hostname,
                        ip.add.re.ss ...)
  -c COMMAND, --command COMMAND
                        Command to run
  --listknown           List known commands
  --getstatus           Get Inverter Status
  --getsettings         Get Inverter Settings
  --printcrc            Display the command and crc and nothing else
  -R, --showraw         Display the raw results
  -v, --version         Display the version
  -D, --debug           Enable Debug and above (i.e. all) messages
  -I, --info            Enable Info and above level messages


```

## Example
run mpp-solar
- giving the 'run' the name FirstInverter
- executing the command QPIRI
- against the inverter connected on /dev/hidraw0
- using protocol PI16
- outputting to the screen

`$ mpp-solar -n 'FirstInverter' -P PI16 -o screen -c QPIRI -p /dev/hidraw0`
```
Parameter                     	Value           Unit
grid_input_voltage_rating     	230.0          	V   
grid_input_frequency_rating   	50.0           	Hz  
grid_input_current_rating     	13.0           	A   
ac_output_voltage_rating      	230.0          	V   
ac_output_current_rating      	13.0           	A   
maximum_input_current_per_pv  	18.0           	A   
battery_voltage_rating        	48.0           	V   
number_of_mpp_trackers        	1              	    
machine_type                  	Hybrid         	    
topology                      	transformerless
```

## Allowing non-root use of hidraw ##

- if you want to be able to use a hidraw device as pi (or other users)
- create a file `/etc/udev/rules.d/99-hidraw.rules` with the below as the content
  ```
  KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0660", GROUP="plugdev"
  ```
  - after a restart (or replug of the USB cable) any user of the plugdev group will be able to read from/write to any /dev/hidraw device

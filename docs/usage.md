# Usage

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
* List commands for protocol PI41
  * `$ mpp-solar -P PI41 -c`
* List output modules available
  * `$ mpp-solar -o`

* Run 'getInfo' command against jkbms BMS with bluetooth MAC '3C:A5:09:0A:AA:AA'
  * `$ jkbms -p 3C:A5:09:0A:AA:AA -c getInfo`

## Troubleshooting / Notes ##
- The commands default to using `/dev/ttyUSB0` if you are using direct USB connection try adding `-p /dev/hidraw0` to the commands
- if you have other USB devices connected the inverter might show up as `/dev/hidraw1` or `/dev/hidraw2`
- if uncertain, remove and re-connect the connection to the inverter and look at the end of the `dmesg` response to see what was reconnected
- also in some instances only root has access to the device that the inverter is connected to - if you are getting no response try using `sudo`
- if you are getting no/unexpected results add `-I` to the command to get some extra information
- if you are getting no/unexpected results add `-D` to the command to get lots of extra information

## mpp-solar arguments
`$ mpp-solar -h`
```
usage: mpp-solar [-h] [-n NAME] [-p PORT] [--porttype PORTTYPE] [-P {PI00,PI16,PI18,PI30,PI41,VED}] [-T TAG] [-b BAUD] [-o [OUTPUT]] [--keepcase] [--filter FILTER]
                 [--exclfilter EXCLFILTER] [-q MQTTBROKER] [--mqttport MQTTPORT] [--mqtttopic MQTTTOPIC] [--mqttuser MQTTUSER] [--mqttpass MQTTPASS] [-c [COMMAND]]
                 [-C [CONFIGFILE]] [--daemon] [--getstatus] [--getsettings] [-v] [-D] [-I]

Solar Device Command Utility, version: 0.7.40, recent changes: add mqtt_topic option and json_mqtt output

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Specifies the device name - used to differentiate different devices
  -p PORT, --port PORT  Specifies the device communications port (/dev/ttyUSB0 [default], /dev/hidraw0, test, ...)
  --porttype PORTTYPE   overrides the device communications port type
  -P {PI00,PI16,PI18,PI30,PI41,VED}, --protocol {PI00,PI16,PI18,PI30,PI41,VED}
                        Specifies the device command and response protocol, (default: PI30)
  -T TAG, --tag TAG     Override the command name and use this instead (for mqtt and influx type output processors)
  -b BAUD, --baud BAUD  Baud rate for serial communications (default: 2400)
  -o [OUTPUT], --output [OUTPUT]
                        Specifies the output processor(s) to use [comma separated if multiple] (screen [default]) leave blank to give list
  --keepcase            Do not convert the field names to lowercase
  --filter FILTER       Specifies the filter to reduce the output - only those fields that match will be output (uses re.search)
  --exclfilter EXCLFILTER
                        Specifies the filter to reduce the output - any fields that match will be excluded from the output (uses re.search)
  -q MQTTBROKER, --mqttbroker MQTTBROKER
                        Specifies the mqtt broker to publish to if using a mqtt output (localhost [default], hostname, ip.add.re.ss ...)
  --mqttport MQTTPORT   Specifies the mqtt broker port if needed (default: 1883)
  --mqtttopic MQTTTOPIC
                        provides an override topic (or prefix) for mqtt messages (default: None)
  --mqttuser MQTTUSER   Specifies the username to use for authenticated mqtt broker publishing
  --mqttpass MQTTPASS   Specifies the password to use for authenticated mqtt broker publishing
  -c [COMMAND], --command [COMMAND]
                        Command to run
  -C [CONFIGFILE], --configfile [CONFIGFILE]
                        Full location of config file (default None, /etc/mpp-solar/mpp-solar.conf if -C supplied)
  --daemon              Run as daemon
  --getstatus           Get Inverter Status
  --getsettings         Get Inverter Settings
  -v, --version         Display the version
  -D, --debug           Enable Debug and above (i.e. all) messages
  -I, --info            Enable Info and above level messages

```

## List available commands for a protocol
To list all the available commands for a given protocol, specify the protocol and `-c` but do not supply a command

`$ mpp-solar -P PI30 -c`
```
Command: command help - List available commands for protocol PI30
------------------------------------------------------------
Parameter                     	Value           Unit
F                             	Set Device Output Frequency	    
MCHGC                         	Set Max Charging Current (for parallel units)	    
MNCHGC                        	Set Utility Max Charging Current (more than 100A) (for 4000/5000)	    
MUCHGC                        	Set Utility Max Charging Current	    
PBCV                          	Set Battery re-charge voltage	    
PBDV                          	Set Battery re-discharge voltage	    
PBFT                          	Set Battery Float Charging Voltage	    
PBT                           	Set Battery Type	    
PCP                           	Set Device Charger Priority	    
PCVV                          	Set Battery C.V. (constant voltage) charging voltage	    
PEPD                          	Set the enabled / disabled state of various Inverter settings (e.g. buzzer, overload, interrupt alarm)	    
PF                            	Set Control Parameters to Default Values	    
PGR                           	Set Grid Working Range	    
POP                           	Set Device Output Source Priority	    
POPM                          	Set Device Output Mode (for 4000/5000)	    
PPCP                          	Set Parallel Device Charger Priority (for 4000/5000)	    
PPVOKC                        	Set PV OK Condition	    
PSDV                          	Set Battery Cut-off Voltage	    
PSPB                          	Set Solar Power Balance	    
Q1                            	Q1 query       	    
QBOOT                         	DSP Has Bootstrap inquiry	    
QDI                           	Default Settings inquiry	    
QFLAG                         	Flag Status inquiry	    
QID                           	Device Serial Number inquiry	    
QMCHGCR                       	Max Charging Current Options inquiry	    
QMOD                          	Mode inquiry   	    
QMUCHGCR                      	Max Utility Charging Current Options inquiry	    
QOPM                          	Output Mode inquiry	    
QPGS                          	Parallel Information inquiry	    
QPI                           	Protocol ID inquiry	    
QPIGS                         	General Status Parameters inquiry	    
QPIRI                         	Current Settings inquiry	    
QPIWS                         	Warning status inquiry	    
QVFW                          	Main CPU firmware version inquiry	    
QVFW2                         	Secondary CPU firmware version inquiry	    
```

or
`$ jkbms -P JK04 -c`
```
ommand: command help - List available commands for protocol JK04
------------------------------------------------------------
Parameter                     	Value           Unit
getInfo                       	BLE Device Information inquiry	    
getCellData                   	BLE Cell Data inquiry
```

## List available output processors
To list all the available output processors, specify `-o` but do not supply any outputs
`$ mpp-solar -o`
```
Command: outputs help - List available output modules
------------------------------------------------------------
Parameter                     	Value           Unit
baseoutput                    	the base class for the output processors, not used directly	    
hass_mqtt                     	outputs the to the supplied mqtt broker in hass format: eg "homeassistant/sensor/mpp_{tag}_{key}/state" 	    
influx2_mqtt                  	outputs the to the supplied mqtt broker: eg mpp-solar,command={tag} max_charger_range=120.0	    
influx_mqtt                   	outputs the to the supplied mqtt broker: eg {tag}, {tag},setting=total_ac_output_apparent_power value=1577.0,unit="VA" 	    
json                          	outputs the results to standard out in json format	    
json_mqtt                     	outputs all the results to the supplied mqtt broker in a single message formated as json: eg 	    
mqtt                          	outputs the results to the supplied mqtt broker: eg {tag}/status/total_output_active_power/value 1250	    
raw                           	outputs the raw results to standard out	    
screen                        	[the default output module] outputs the results to standard out in a slightly formatted way	    
tag_mqtt                      	outputs the to the supplied mqtt broker using the supplied tag as the topic: eg {tag}/max_charger_range 120.0	    
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


# JKBMS Usage #
```
$ jkbms -h
usage: jkbms [-h] [-n NAME] [-p PORT] [--porttype PORTTYPE] [-P {JK02,JK04,JK485}] [-T TAG] [-b BAUD] [-M MODEL] [-o [OUTPUT]] [-q MQTTBROKER] [--mqttuser MQTTUSER]
             [--mqttpass MQTTPASS] [-c [COMMAND]] [-C CONFIGFILE] [--daemon] [--getstatus] [--getsettings] [-R] [-v] [-D] [-I]

Solar Device Command Utility, version: 0.7.19, recent changes: fix json output

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Specifies the device name - used to differentiate different devices
  -p PORT, --port PORT  Specifies the device communications port (/dev/ttyUSB0 [default], /dev/hidraw0, test, ...)
  --porttype PORTTYPE   overrides the device communications port type
  -P {JK02,JK04,JK485}, --protocol {JK02,JK04,JK485}
                        Specifies the device command and response protocol, (default: JK04)
  -T TAG, --tag TAG     Override the command name and use this instead (for mqtt and influx type output processors)
  -b BAUD, --baud BAUD  Baud rate for serial communications (default: 2400)
  -M MODEL, --model MODEL
                        Specifies the inverter model to select commands for, defaults to "standard", currently supports LV5048
  -o [OUTPUT], --output [OUTPUT]
                        Specifies the output processor(s) to use [comma separated if multiple] (screen [default]) leave blank to give list
  -q MQTTBROKER, --mqttbroker MQTTBROKER
                        Specifies the mqtt broker to publish to if using a mqtt output (localhost [default], hostname, ip.add.re.ss ...)
  --mqttuser MQTTUSER   Specifies the username to use for authenticated mqtt broker publishing
  --mqttpass MQTTPASS   Specifies the password to use for authenticated mqtt broker publishing
  -c [COMMAND], --command [COMMAND]
                        Command to run
  -C CONFIGFILE, --configfile CONFIGFILE
                        Full location of config file
  --daemon              Run as daemon
  --getstatus           Get Inverter Status
  --getsettings         Get Inverter Settings
  -R, --showraw         Display the raw results
  -v, --version         Display the version
  -D, --debug           Enable Debug and above (i.e. all) messages
  -I, --info            Enable Info and above level messages

  ```

```
$ jkbms -P JK02 -c
Parameter                     	Value           Unit
getInfo                       	BLE Device Information inquiry	    
getCellData                   	BLE Cell Data inquiry
```

```
$ jkbms -p 3C:A5:09:0A:AA:AA -c getInfo
Command: getInfo - BLE Device Information inquiry
------------------------------------------------------------
Parameter                     	Value           Unit
Header                        	55aaeb90       	    
Record Type                   	03             	    
Record Counter                	181            	    
Device Model                  	JK-BD6A20S     	    
Hardware Version              	10P4.0         	    
Software Version              	4.1.7          	    
Device Name                   	JK-BD6A20S    	    
Device Passcode               	xxxx          	    
Unknown1                      	200708         	    
Unknown2                      	2006284075     	    
User Data                     	Input Userdata 	    
Settings Passcode?            	xxx         
```

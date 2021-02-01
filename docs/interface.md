# Inteface / How it all hangs together #

* First is a **DEVICE** instance (one of the non-abstract classes from mppsolar/devices)
    * mppsolar
    * ...

* The DEVICE will (should) set an **IO PORT** (one of the non-abstract classes from mppsolar/io)
    * esp32io
    * hidrawio
    * serialio
    * testio
    * ...

* and a **PROTOCOL** (one of the non-abstract classes from mppsolar/protocols)
    * pi16
    * pi18
    * pi30
    * pi41
    * ...

* a result will be obtained by running a command
* the results *dict* will be output via 1 or more **OUTPUTS** (one of the non-abstract classes from mppsolar/outputs)
    * screen
    * mqtt
    * influx_mqtt
    * influx2_mqtt
    * ...

## DEVICE classes ##
* Should initialize with name, port and protocol
    * `device = device_class(name=args.name, port=args.port, protocol=args.protocol)`
* and define the following functions:
```
__str__(self) -> str
run_command(self, command) -> dict
get_status(self) -> dict
get_settings(self) -> dict
```

These functions are called based on the command line (or service) options

_Generally speaking_ the DEVICE will run commands via the IO PORT using the PROTOCOL, e.g.
```
def run_command(self, command) -> dict:
      log.info(f"Running command {command}")
      [...snip...]
      response = self._port.send_and_receive(command, self._protocol)
      return response
```



## IO PORT classes ##
* Should inherit from the BaseIO class, e.g: `class ESP32IO(BaseIO)`
* and define the function:
```
send_and_receive(self, command, protocol) -> dict
```
_Generally speaking_ the IO PORT will use the PROTOCOL decode function to build the response dict
```
decoded_response = protocol.decode(response_line)
```


## PROTOCOL classes ##
* Generally inherits from the AbstractProtocol base class
* define the following functions:
    * `get_full_command(self, command) -> bytes:`
    * `get_command_defn(self, command) -> dict:` (from AbstractProtocol)
    * `decode(self, response) -> dict:` (default uses get_responses)


## OUTPUTS ##
* Define a single function:
```
output(self, data, tag, mqtt_broker, mqtt_user, mqtt_pass) -> None
```
This function performs the outputing of the data and expects a dict like below (for a simple response)
`{'serial_number': ['9293333010501', ''], '_command': 'QID', '_command_description': 'Device Serial Number inquiry'}`

```
print(f"{'Parameter':<30}\t{'Value':<15} Unit")
    for key in data:
        value = data[key][0]
        unit = data[key][1]
        print(f"{key:<30}\t{value:<15}\t{unit:<4}")
```

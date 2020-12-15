# Inteface / How it all hangs together #

* First is a DEVICE instance (one of the non-abstract classes from mppsolar/devices)
    * mppsolar
    * ...

* The DEVICE will (should) set an IO PORT (one of the non-abstract classes from mppsolar/io)
    * esp32io
    * hidrawio
    * serialio
    * testio
    * ...

* and a PROTOCOL (one of the non-abstract classes from mppsolar/protocols)
    * pi16
    * pi18
    * pi30
    * pi41
    * ...


## DEVICE classes ##
* Should inherit from the AbstractDevice class, e.g: `class mppsolar(AbstractDevice)`
* and define the following functions:
    * __str__(self) -> str
    * run_command(self, command, show_raw) -> dict
    * get_status(self, show_raw) -> dict
    * get_settings(self, show_raw) -> dict
    * run_default_command(self, show_raw) -> dict

These functions are called based on the command line (or service) options

_Generally speaking_ the DEVICE will run commands via the IO PORT using the PROTOCOL, e.g.
```
def run_command(self, command, show_raw=False) -> dict:
      """
      mpp-solar specific method of running a 'raw' command, e.g. QPI or PI
      """
      log.info(f"Running command {command}")
      [...snip...]
      response = self._port.send_and_receive(command, show_raw, self._protocol)
      return response
```


## IO PORT classes ##
* Should inherit from the BaseIO class, e.g: `class ESP32IO(BaseIO)`
* and define the function:
    * send_and_receive(self, command, show_raw, protocol) -> dict

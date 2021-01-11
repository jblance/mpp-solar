## Troubleshooting / Notes ##
- The commands default to using `/dev/ttyUSB0` if you are using direct USB connection try adding `-d /dev/hidraw0` to the commands
- if you have other USB devices connected the inverter might show up as `/dev/hidraw1` or `/dev/hidraw2`
- if uncertain, remove and re-connect the connection to the inverter and look at the end of the `dmesg` response to see what was reconnected
- also in some instances only root has access to the device that the inverter is connected to - if you are getting no response try using `sudo`
- if you are getting no/unexpected results add `-I` to the command to get some extra information
- if you are getting no/unexpected results add `-D` to the command to get lots of extra information

## Allowing non-root use of hidraw ##

- if you want to be able to use a hidraw device as pi (or other users)
- make sure the pi user is in the plugdev group `sudo usermod -a -G plugdev pi`
- create a file `/etc/udev/rules.d/99-hidraw.rules` with the below as the content
  ```
  KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0660", GROUP="plugdev"
  ```
  - after a restart (or replug of the USB cable) any user of the plugdev group will be able to read from/write to any /dev/hidraw device  
  - check with `ls -l /dev/hidraw*`
```
crw-rw---- 1 root plugdev 245, 0 Oct 15 03:17 /dev/hidraw0
```

## JKBMS ##

### Requirements ###
* bluepy `sudo pip3 install bluepy`
* paho-mqtt if publishing to MQTT `sudo pip3 install paho-mqtt`
* a device with BLE support (Raspberry Pi 3 or 4 have BLE builtin)

### Troubleshooting ###
* Make sure the JK App is getting data correctly
* Do a BLE scan (outside of python) `sudo hcitool lescan`
```
$ sudo hcitool lescan
LE Scan ...
3C:A5:09:0A:AA:AA (unknown)
3C:A5:09:0A:AA:AA JK-B2A24S
```
* Try debuging without `mpp-solar -p <mac address> -P JK04 -D`
* Log an issue with the above information

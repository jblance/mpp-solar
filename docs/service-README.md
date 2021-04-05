# Installing as a Service #
source: https://github.com/torfsen/python-systemd-tutorial

## Pre-reqs ##
Need python-systemd package
* `sudo apt-get install python3-systemd`
* or `pip install systemd-python`

Need to create a config file `/etc/mpp-solar/mpp-solar.conf`
* Use the example [mpp-solar example](service/mpp-solar.conf.example) as a start

[see here for examples](configfile.md#Config-file-examples)

## Add mpp-solar service ##
* Create a unit file `/etc/systemd/user/mpp-solar.service`
  * copy [mpp-solar](service/mpp-solar.service) to `/etc/systemd/user/mpp-solar.service`
* Check the service exists
`systemctl --user list-unit-files|grep mpp-solar`
```
mpp-solar.service              disabled
```
* Start the service
`systemctl --user start mpp-solar`

* Check service status
`systemctl --user status mpp-solar`
```
● mpp-solar.service - MPP Solar Service
   Loaded: loaded (/etc/systemd/user/mpp-solar.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2021-04-06 08:20:45 NZST; 3h 2min ago
 Main PID: 2682 (python3)
   CGroup: /user.slice/user-1000.slice/user@1000.service/mpp-solar.service
           └─2682 /usr/bin/python3 /usr/local/bin/mpp-solar -C /etc/mpp-solar/mpp-solar.conf --daemon

Apr 06 11:22:51 batteryshed python3[2682]: Getting results from device: mppsolar device - name: Inverter_2, port: <mppsolar.io.hidrawio.HIDRawIO object at 0x75cd5290>
Apr 06 11:22:55 batteryshed python3[2682]: Getting results from device: mppsolar device - name: Inverter_2, port: <mppsolar.io.hidrawio.HIDRawIO object at 0x75cd5290>
Apr 06 11:22:57 batteryshed python3[2682]: Getting results from device: mppsolar device - name: Inverter_2, port: <mppsolar.io.hidrawio.HIDRawIO object at 0x75cd5290>
Apr 06 11:23:00 batteryshed python3[2682]: Sleeping for 1 sec
Apr 06 11:23:01 batteryshed python3[2682]: Getting results from device: mppsolar device - name: Inverter_1, port: <mppsolar.io.serialio.SerialIO object at 0x75ed4ff0>
...
```

* Stopping the service
`systemctl --user stop mpp-solar`

* Restart the service - for example after a config file change
`systemctl --user restart mpp-solar`

Logs and service output
* The output should show up in systemd's logs, which by default are redirected to syslog:
`grep 'mppsolar' /var/log/syslog`
```
Apr  6 11:27:20 batteryshed python3[2682]: Getting results from device: mppsolar device - name: Inverter_2, port: <mppsolar.io.hidrawio.HIDRawIO object at 0x75cd5290>, protocol: <mppsolar.protocols.pi30.pi30 object at 0x75ed4f30> for command: Q1, tag: Inverter2, outputs: hass_mqtt
Apr  6 11:27:22 batteryshed python3[2682]: Getting results from device: mppsolar device - name: Inverter_2, port: <mppsolar.io.hidrawio.HIDRawIO object at 0x75cd5290>, protocol: <mppsolar.protocols.pi30.pi30 object at 0x75ed4f30> for command: QPIGS, tag: Inverter2, outputs: hass_mqtt
Apr  6 11:27:25 batteryshed python3[2682]: Sleeping for 1 sec
```

* Another way to display the service's output is via
`journalctl --user-unit mpp-solar`

## Automatically Starting the Service during Boot ##
```
systemctl --user enable mpp-solar
sudo loginctl enable-linger $USER
```

* To disable autostart, simply disable your service:
`systemctl --user disable mpp-solar`

Note that simply enabling a service does not start it, but only activates autostart during boot-up. Similarly, disabling a service doesn't stop it, but only deactivates autostart during boot-up. If you want to start/stop the service immediately then you still need to do that manually

To check whether your service is enabled, use

`systemctl --user list-unit-files | grep mpp-solar`
```
mpp-solar.service              enabled
```

# Creating a System Service #
Once you have a working user service you can turn it into a system service. Remember, however, that system services run in the system's central systemd instance and have a greater potential for disturbing your system's stability or security when not implemented correctly. In many cases, this step isn't really necessary and a user service will do just fine.

## Stopping and Disabling the User Service ##
Before turning our service into a system service let's make sure that its stopped and disabled. Otherwise we might end up with both a user service and a system service.
```
$ systemctl --user stop mpp-solar
$ systemctl --user disable mpp-solar
```
## Moving the Unit File ##
/etc/systemd/user/mpp-solar.service
Previously, we stored our unit file in a directory appropriate for user services (`/etc/systemd/user/mpp-solar.service`). As with user unit files, systemd looks into more than one directory for system unit files. We'll be using `/etc/systemd/user/mpp-solar.service`, so move your unit file there and make sure that it has the right permissions
```
$ sudo mv /etc/systemd/user/mpp-solar.service /etc/systemd/system/
$ sudo chown root:root /etc/systemd/system/mpp-solar.service
$ sudo chmod 644 /etc/systemd/system/mpp-solar.service
```
Our service is now a system service! This also means that instead of using `systemctl --user ...` we will now use `systemctl ...` (without the `--user` option) instead (or `sudo systemctl ...` if we're modifying something). For example:
```
$ systemctl list-unit-files | grep mpp-solar
python_demo_service.service                disabled
```
Similarly, use `journalctl --unit mpp-solar` to display the system service's logs.


## troubleshooting ##
```
Traceback (most recent call last):
  File "/home/pi/venv/mppsolar/bin/mpp-solar", line 11, in <module>
    load_entry_point('mpp-solar', 'console_scripts', 'mpp-solar')()
  File "/home/pi/venv/mppsolar/src/mpp-solar/mppsolar/__init__.py", line 211, in main
    systemd.daemon.notify("READY=1")
  File "/home/pi/venv/mppsolar/lib/python3.7/site-packages/systemd/daemon.py", line 39, in notify
    raise TypeError("state must be an instance of Notification")
TypeError: state must be an instance of Notification
```
have systemd instead of systemd-python
$ pip uninstall systemd
$ pip install systemd-python
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Collecting systemd-python
  Downloading https://www.piwheels.org/simple/systemd-python/systemd_python-234-cp37-cp37m-linux_armv7l.whl (179kB)
    100% |████████████████████████████████| 184kB 51kB/s
Installing collected packages: systemd-python
Successfully installed systemd-python-234

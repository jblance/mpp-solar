# Installing as a Service #
source: https://github.com/torfsen/python-systemd-tutorial

## Pre-reqs ##
Need python-systemd package
* `sudo apt-get install python-systemd`

Need to create a config file `/etc/mpp-solar/mpp-solar.conf`
* Use the example `/etc/mpp-solar/mpp-solar.conf.example` as a start

## Add mpp-solar service ##

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
mpp-solar.service - MPP Solar Service
   Loaded: loaded (/etc/systemd/user/mpp-solar.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2020-04-08 16:19:46 NZST; 10s ago
 Main PID: 21724 (python)
   CGroup: /user.slice/user-1000.slice/user@1000.service/mpp-solar.service
           └─21724 /usr/bin/python /usr/local/bin/mpp-solar-service -c /etc/mpp-solar/mpp-solar.conf

Apr 08 16:19:46 batteryshed python[21724]: MPP-Solar-Service: Config file: /etc/mpp-solar/mpp-solar.conf
Apr 08 16:19:46 batteryshed python[21724]: MPP-Solar-Service: Config setting - pause: 1
Apr 08 16:19:46 batteryshed python[21724]: MPP-Solar-Service: Config setting - mqtt_broker: mqtthost
Apr 08 16:19:46 batteryshed python[21724]: MPP-Solar-Service: Config setting - command sections found: 2
...
```

* Stopping the service
`systemctl --user stop mpp-solar`

* Restart the service - for example after a config file change
`systemctl --user restart mpp-solar`

* Logs and service output
* The output should show up in systemd's logs, which by default are redirected to syslog:
`grep 'MPP-Solar-Service' /var/log/syslog`
```
Apr  8 16:23:27 batteryshed python[21724]: MPP-Solar-Service: item {'tag': u'QPGS0', 'command': u'QPGS0', 'mp': <mppsolar.mpputils.mppUtils instance at 0x75d61c88>, 'format': u'influx2'}
Apr  8 16:23:30 batteryshed python[21724]: MPP-Solar-Service: item {'tag': u'QPGS1', 'command': u'QPGS1', 'mp': <mppsolar.mpputils.mppUtils instance at 0x75d61df0>, 'format': u'influx2'}
Apr  8 16:23:32 batteryshed python[21724]: MPP-Solar-Service: sleeping for 1sec
```

* Another way to display the service's output is via
`journalctl --user-unit mpp-solar`

## Automatically Starting the Service during Boot ##
`systemctl --user enable mpp-solar`
`sudo loginctl enable-linger $USER`

* To disable autostart, simply disable your service:
`systemctl --user disable python_demo_service`

Note that simply enabling a service does not start it, but only activates autostart during boot-up. Similarly, disabling a service doesn't stop it, but only deactivates autostart during boot-up. If you want to start/stop the service immediately then you still need to do that manually

To check whether your service is enabled, use

`systemctl --user list-unit-files | grep mpp-solar`
```
mpp-solar.service              enabled
```

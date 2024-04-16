# MPP_Solar

Dashboards homepage can be found at:
https://github.com/cordelster/mppsolar_dashboards

## Gauge and graph:
![Grafana dashboard](https://github.com/cordelster/mppsolar_dashboards/blob/main/prometheus/pics/dash_guages.png)

## Stats as table:
![Grafana dashboard stats in table](https://github.com/cordelster/mppsolar_dashboards/blob/main/prometheus/pics/dash_tables.png)


You can also find these instructions on the top row within the dashboard.
This Dashboard takes avantage of using prom output from mpp_solar with command output from QPGS and QPIGS.
This output can be directed to a text file while building the file, then moved to node_exporter folder as a prom file.
This works with all *nix.

Requires a working installation of Prometheus_node_exporter on the same system with collection from folder enabled for node_exporter. Here is an example though I use an rc busybox based OS and your init system is likelly Systemd. The important part is to add a folder for node_exporter to read the prometheus formated files and enable node_exporter to do so ` --collector.textfile.directory=/var/lib/node-exporter/mppsolar` and your needs of where to add this switch will depend on your choice of distribution.

```
# cat /etc/init.d/node-exporter-mpp
#!/sbin/openrc-run
supervisor=supervise-daemon

command="/usr/bin/node_exporter"
command_args="--no-collector.mdadm --collector.textfile.directory=/var/lib/node-exporter/mppsolar $ARGS"
command_background="yes"
group="prometheus"
user="prometheus"

logdir="/var/log/prometheus"
logfile="$logdir/${SVCNAME}.log"
datadir="/tmp/mppsolar"
pidfile="/var/run/${SVCNAME}.pid"
start_stop_daemon_args="--stderr $logfile --user $user --group $group"

depend() {
	need net
	after firewall
}

start_pre() {
	checkpath -d -o $user:$group -m755 $logdir
	checkpath -f -o $user:$group -m644 $logfile
        checkpath -f -o $user:$group -m755 $datadir
}
```


Designed for Rich Solar 6548 and should work for MPP LV6548 and the like. Should also work with other inverters though thresholds should be adjusted for each case based on the models abilities.

Adjust your serial ports as needed. 

`Example configurations:`
```
# cat /etc/mppsolar/mpp_qpgs.conf
[SETUP]
pause=5

[Inverter_2]
port=/dev/ttyUSB2
protocol=PI30max
command=QPGS2
tag=QPGS2
outputs=prom
dev=SCC2

[Inverter_1]
port=/dev/ttyUSB0
protocol=PI30max
command=QPGS1
tag=QPGS1
outputs=prom
dev=SCC1
```


```
 # cat /etc/mppsolar/mpp_qpigs.conf
 # This output required for Inverter heatsink temp, and PV1 charge wattage.
[SETUP]
pause=5

[Inverter_2]
port=/dev/ttyUSB2
protocol=PI30max
command=QPIGS
outputs=prom
dev=SCC2

[Inverter_1]
port=/dev/ttyUSB0
protocol=PI30max
command=QPIGS
outputs=prom
dev=SCC1
```
```
# cat /etc/mppsolar/mpp_qpigs2.conf
### This config for inverters with more than one PV input, to retrive PV2 Charge Wattage output.
### Thoogh not a requirement with this dashboard.
[SETUP]
pause=5

[Inverter_2]
port=/dev/ttyUSB2
protocol=PI30max
command=QPIGS2
outputs=prom
dev=SCC2

[Inverter_1]
port=/dev/ttyUSB0
protocol=PI30max
command=QPIGS2
outputs=prom
dev=SCC1
```
Executable in /usr/local/bin/
```
# cat /usr/local/bin/mpp-get-data.sh
#!/bin/ash
dataFile="mppsolar"
dataDir="/var/lib/node-exporter/mppsolar/"

checkpath -d "$dataDir" -m 755 -o prometheus:prometheus

while : ; do

        `/usr/bin/mpp-solar -C /etc/mppsolar/mpp_qpgs.conf > ${dataDir}${dataFile}.$$` && \
        `/usr/bin/mpp-solar -C /etc/mppsolar/mpp_qpigs.conf >> ${dataDir}${dataFile}.$$` && \
        `/usr/bin/mpp-solar -C /etc/mppsolar/mpp_qpigs2.conf >> ${dataDir}${dataFile}.$$` && \
        mv ${dataDir}${dataFile}.$$ ${dataDir}${dataFile}.prom
        sleep 5
done
```

Create a SysV or systemd startup for the executable.

For markdown syntax help: [commonmark.org/help](https://commonmark.org/help/)

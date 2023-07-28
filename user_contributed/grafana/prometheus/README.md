# MPP_Solar

You can also find these instructions on the top row within the dashboard.
This Dashboard takes avantage of using prom output from mpp_solar with command output from QPGS and QPIGS.
This output can be directed to a text file while building the file, then moved to node_exporter folder as a prom file.

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

checkpath -d "$dataDir" -m 755 -o node_exporter:node_exporter

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

# Voltronic Power SUNNY Protocol #

* Daniele Pezzini <hyouko@gmail.com>
* v1.2, July 2015
* https://github.com/zykh/nut-website/blob/voltronic-sunny/protocols/voltronic-sunny.txt

This document describes the protocol used in Voltronic Power <<protocol,P15>> and <<protocol,P16>> solar devices.


## Communication ##
* RS232C
  * 9 pins female D-type connector - only 3 wires: TX, RX (crossed)  and GND
  * Baud rate:::	2400 bps
  * Data length:::	8 bits
  * Stop bit:::	1 bit
	* Parity:::	none
* USB
	* Serial over USB with 'cypress' protocol


## Accepted queries and commands ##

All commands, queries and device's replies are terminated by +<cr>+.
Optionally, before the trailing +<cr>+, the device, in its replies, may put a 2-bytes non-reflected CRC (polynomial: 0x1021) with +<lf>+, +<cr>+ and +(+ 'escaped'

Command begginning with *+Q+* -> query.


## Device replies ##
- *+(ACK+* -> Command accepted
- *+(NAK+* -> Command/Query rejected or invalid


## Device status ##

### *+QPIGS+* ###
Query device for status

Reply
```
(AAA.A BBBBBB CC.C DDDD.D EEE.E FFFFF GG.G HHH.H III JJJ.J KKK.K LLL.L MMM.M NNN OOOOO PPPPP QQQQQ RRR.R SSS.S TTT.T UUU.U VWWWWWWWWW
```
.e.g.
```
(226.1 000378 50.0 0001.7 226.8 00378 49.9 001.6 013 436.4 436.4 052.6 ---.- 077 00920 00292 ----- 196.1 ---.- ---.- 027.0 A---101001
  ```

Where:
```
+AAA.A+::	Grid voltage (V)
+BBBBBB+::	Output power (W)
+CC.C+::	Grid frequency (Hz)
+DDDD.D+::	Output current (A)
+EEE.E+::	AC output voltage R (V)
+FFFFF+::	AC output power R (W)
+GG.G+::	AC output frequency (Hz)
+HHH.H+::	AC output current R (A)
+III+::		Output load percent (%)
+JJJ.J+::	PBUS voltage (V)
+KKK.K+::	SBUS voltage (V)
+LLL.L+::	Positive battery voltage (V)
+MMM.M+::	Negative battery voltage (V)
+NNN+::		Battery capacity (%)
+OOOOO+::	PV1 input power (W)
+PPPPP+::	PV2 input power (W)
+QQQQQ+::	PV3 input power (W)
+RRR.R+::	PV1 input voltage (V)
+SSS.S+::	PV2 input voltage (V)
+TTT.T+::	PV3 input voltage (V)
+UUU.U+::	Max temperature (°C)
+V+::		*{sp}unknown *
+WWWWWWWWW+::	Device status, where each index (b8..b0) means (not supported options have the corresponding indexes filled with `++-++'):

[cols="^.^1m,.^9"]
|====
|bit#	|Description
|8	a|Connection to the grid status:

	- +0+ -> disconnected
	- +1+ -> connected
|7	|*{sp}unknown *
|6	|*{sp}unknown *
|5	a|Load status

	- +0+ -> device doesn't have load
	- +1+ -> device has load
|4	.2+a|Battery status

	- +00+ -> battery not connected
	- +01+ -> charging
	- +10+ -> discharging
|3
|2	a|Inverter direction:

	- +0+ -> DC-to-AC
	- +1+ -> AC-to-DC
	- +2+ -> *{sp}unknown *
|1	.2+a|Line direction:

	- +00+ -> both taking from grid and feeding grid
	- +01+ -> taking from grid
	- +10+ -> feeding grid
|0
|====
```

## *+QPIBI+* ##
Query device for battery information (<<protocol,P16>> only)
Reply
```
(AAA BBB CCC DDD EEE
```
e.g.
```
(000 001 002 003 004
```

Where:
```
+AAA+::	*{sp}unknown *
+BBB+::	Number of batteries
+CCC+::	Battery total capacity (Ah)
+DDD+::	*{sp}unknown *
+EEE+::	Battery remaining time (minutes)
```

## *+QMOD+* ##
Query device for actual operational mode

If <<protocol,P15>>, or if <<protocol,P16>> *and* <<mt,model type *is* Grid-tie''>>, possible replies are:
```
+(D+::			<<shutdown-mode,Shutdown Mode>>
+(F+::			<<fault-mode,Fault Mode>>
+(G+::			<<grid-mode,Grid Mode>>
+(L+::			<<line-mode,Line Mode>>
+(P+::			<<power-on-mode,Power on Mode>>
+(S+::			<<standby-mode,Standby Mode>>
+(Y+::			<<bypass-mode,Bypass Mode>>
+(B+::
+(C+::
+(T+::
all other cases::	<<standby-mode,Standby Mode>>

If <<protocol,P16>> *and* <<mt,model type *is not* Grid-tie''>>, possible replies are:

+(B+::			<<inverter-mode,Inverter (Battery) Mode>>
+(C+::			Depending on conditions, it means:
			- <<bypass-w-pvchrg-mode,Bypass with PV charging Mode>>
			- <<standby-w-pvchrg-mode,Standby with PV charging Mode>>
+(F+::			Fault; plus, depending on conditions, it means:
			- <<bypass-w-pvchrg-mode,Bypass with PV charging Mode>>
			- <<bypass-wo-chrg-mode,Bypass without charging Mode>>
			- <<standby-w-pvchrg-mode,Standby with PV charging Mode>>
			- <<standby-wo-chrg-mode,Standby without charging Mode>>
+(G+::			Depending on conditions, it means:
			- <<grid-tie-w-backup-mode,Grid-tie with backup Mode>>
			- <<bypass-w-acchrg-mode,Bypass with AC charging Mode>>
			- <<standby-w-acchrg-mode,Standby with AC charging Mode>>
			- <<standby-wo-chrg-mode,Bypass without charging Mode>>
+(P+::			<<power-on-mode,Power on Mode>>
+(S+::			<<standby-wo-chrg-mode,Standby without charging Mode>>
+(Y+::			<<bypass-wo-chrg-mode,Bypass without charging Mode>>
all other cases::	<<standby-mode,Standby Mode>>
--
```

```
*+QPIWS+*::	Query device for warning status
+
--
.Reply
----
(b0b2..b126b127
----
.e.g.
----
(--0000000000--00000---00000-----------------------------------------------------------------------------------------------------
----
Each bit corresponds to an error/warning (-> see <<warnings,'Warnings'>>) and its value signals the status of the error/warning:

- +1+ -> error/warning present;
- +0+ -> no warning/error;
- +-+ -> specific warning/error not supported.
--
```

```
*+QPIFS+*::			Query device for faults and their type.
				Available only if <<fw,FW version>> is < in <<protocol,P15>>: 0.9; in <<protocol,P16>>: 0.3.
				To be used only if the device <<warning-status,reports>> it <<device-fault,has faults>>.
+
--
.Reply
----
(AA BBBBBBBBBBBBBB CCC DDD EEE FFF GGG HHH III JJJ KKK LLL MMM NNN OOO PPP QQQ RRR SSS TTT
----
.e.g.
----
(14 20140102221215 000 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017
----

Where:

+AA+::			Type of fault found (-> see <<faults,'Faults'>>)
+BBBBBBBBBBBBBB+::	Fault date (+YYYYMMDDhhmmss+ format)
+CCC+::			PV1 input voltage (V)
+DDD+::			PV1 input current (A)
+EEE+::			PV2 input voltage (V)
+FFF+::			PV2 input current (A)
+GGG+::			PV3 input voltage (V)
+HHH+::			PV3 input current (A)
+III+::			Inverter voltage (V)
+JJJ+::			Inverter current (A)
+KKK+::			Grid voltage (V)
+LLL+::			Grid frequency (Hz)
+MMM+::			Grid current (A)
+NNN+::			Output load percent (%)
+OOO+::			Output load current (A)
+PPP+::			Output load voltage (V)
+QQQ+::			Output load frequency (Hz)
+RRR+::			Battery voltage (V)
+SSS+::			Max temperature (°C)
+TTT+::			Run status

.Alternative reply
----
(OK
----
-> No fault
--
```

```
*+QPICF+*::			Query device for faults and their type.
				Available only if <<fw,FW version>> is >= in <<protocol,P15>>: 0.9; in <<protocol,P16>>: 0.3.
+
--
.Reply
----
(AA BB
----
.e.g.
----
(01 02
----

Where:

+AA+::			Fault status
[[fault-id]]+BB+::	Fault ID
--
```

```
*+QPIHF<n>+*::			Query device for fault *+<n>+* (2 digit integer, +NN+, <<fault-id,fault ID as reported by the device>>), and its type.
				Available only if <<fw,FW version>> is >= in <<protocol,P15>>: 0.9; in <<protocol,P16>>: 0.3.
+
--
.Reply
----
(AA BBBBBBBBBBBBBB CCC DDD EEE FFF GGG HHH III JJJ KKK LLL MMM NNN OOO PPP QQQ RRR SSS TTT
----
.e.g.
----
(14 20140102221215 000 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017
----

Where:

+AA+::			Type of fault found (-> see <<faults,'Faults'>>)
+BBBBBBBBBBBBBB+::	Fault date (+YYYYMMDDhhmmss+ format)
+CCC+::			PV1 input voltage (V)
+DDD+::			PV1 input current (A)
+EEE+::			PV2 input voltage (V)
+FFF+::			PV2 input current (A)
+GGG+::			PV3 input voltage (V)
+HHH+::			PV3 input current (A)
+III+::			Inverter voltage (V)
+JJJ+::			Inverter current (A)
+KKK+::			Grid voltage (V)
+LLL+::			Grid frequency (Hz)
+MMM+::			Grid current (A)
+NNN+::			Output load percent (%)
+OOO+::			Output load current (A)
+PPP+::			Output load voltage (V)
+QQQ+::			Output load frequency (Hz)
+RRR+::			Battery voltage (V)
+SSS+::			Max temperature (°C)
+TTT+::			Run status
--
```

```
*+QFLAG+*::			Query device for capability flag; only those capabilities whom the device is capable of are reported as enabled or disabled
+
--
.Reply
----
(EaaaDbbb
----
.e.g.
----
(EbgpDa
----

Where:

+a..a+::	Enabled options
+b..b+::	Disabled options
--
[[reset-to-default]]*+PF+*::	Set all capability options and their limits to <<default,safe default values>> (*doable only in <<standby-mode,Standby Mode>>*)
*+PE<x>+*::			Enable *+<x>+* option
*+PD<x>+*::			Disable *+<x>+* option

.Available options
[[alarm-control]]*+A+*::	Alarm control (BEEP!)
*+B+*::				Alarm at <<inverter-mode,Inverter (Battery) Mode>> (-> the alarm will beep only if <<alarm-control,alarm control>>, if available, is enabled)
*+G+*::				Green power function (energy saving -> auto off when there is no load)
*+P+*::				Alarm at <<bypass-mode,Bypass Mode>> (-> the alarm will beep only if <<alarm-control,alarm control>>, if available, is enabled)
```

Operational options (<<protocol,P16>> only)
```
*+QENF+*::			Query device for operational options flag
+
--
.Reply
----
(AxBxCxDxExFxGxHxIxJx
----
.e.g.
----
(A1B0C1D0E1F0G0H0I_J_
----

Where:

+A+, ..., +J+::	Available options
+x+::		Option status:
		- +0+ -> disabled
		- +1+ -> enabled
		- +_+ -> not supported
--
*+ENF<option><action>+*::	Enable (*+<action>+*: +1+) or disable (*+<action>+*: +0+) *+<option>+* option

.Available options
[[oops-a]]*+A+*::	Allow to charge battery.
			- If enabled and there is enough PV power (eventually after supporting the load), it will charge battery.
			- If disabled, battery will not be charged.
[[oops-b]]*+B+*::	Allow AC to charge battery.
			- If enabled and <<oops-a,PV power>> is not sufficient, grid will charge battery.
			- If disabled, grid will not charge battery.
[[oops-c]]*+C+*::	Allow to feed-in to the grid.
[[oops-d]]*+D+*::	Allow battery to discharge when PV is available.
			- If enabled, when PV power is available, but it’s not sufficient, battery will provide power to the load.
			  When battery power is running out or not available, grid will back up the load.
			- If disabled, when PV power is available, but it's not sufficient, grid will provide power to the load.
			  When grid is not available at the same time, battery power will back up.
[[oops-e]]*+E+*::	Allow battery to discharge when PV is unavailable.
+
--
			- If enabled, when PV power is not available, battery will provide power to the load at first.
			  When battery power is running out, grid will back up the load.
			- If disabled, when PV power is not available, grid will provide power to the load at first.
			  When grid is not available, battery will provide power backup.
--
+
--
NOTE:			This option will become ineffective during <<ct,AC charging time>> and the priority will automatically become: 1. Grid, 2. Battery.
			Otherwise, it will cause battery damage.
--
[[oops-f]]*+F+*::	Allow battery to feed-in to the grid when PV is available.
[[oops-g]]*+G+*::	Allow battery to feed-in to the grid when PV is unavailable.
*+H+*::			*{sp}unknown *
*+I+*::			*{sp}unknown *
*+J+*::			*{sp}unknown *
```

Generator as AC source option (<<protocol,P16>> only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*+GNTMQ+*::		Query device for generator as AC source option status
+
--
.Reply
----
(AB
----
.e.g.
----
(00
----

Where:

+A+::	*{sp}unknown *
+B+::	Option status:
	- +0+ -> disabled
	- +1+ -> enabled
--
*+GNTM<action>+*::	Enable (*+<action>+*: +1+) or disable (*+<action>+*: +0+) generator as AC source option


[[priority]]
PV energy supply priority (<<protocol,P16>> only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*+QPRIO+*::	Query device for <<mt,PV energy supply priority>>
+
--
.Reply
----
(AA
----
.e.g.
----
(01
----

Where:

+AA+::	<<mt,PV energy supply priority>>
--
*+PRIO<n>+*::	Set <<mt,PV energy supply priority>> to *+<n>+* (2 digit integer, +NN+)


Rated informations


[[protocol]]*+QPI+*::	Query device for protocol
+
--
.Reply
----
(PINN
----
.e.g.
----
(PI15
----

Where:

+NN+::	Protocol used by the device, acceptable values are:
	- +15+
	- +16+
--
[[fw]]*+QSVFW2+*::	Query device for firmware version
+
--
.Reply
----
(SVERFW2:AAAAA.AA
----
.e.g.
----
(SVERFW2:00000.48
----

Where:

+AAAAA.AA+::	Firmware version
--
*+QVFW+*::		Query device for main CPU processor version
+
--
.Reply
----
(VERFW:AAAAA.AA
----
.e.g.
----
(VERFW:00003.10
----

Where:

+AAAAA.AA+::	Main CPU processor version
--
*+QVFW2+*::		Query device for secondary CPU processor version
+
--
.Reply
----
(VERFW2:AAAAA.AA
----
.e.g.
----
(VERFW2:00000.31
----

Where:

+AAAAA.AA+::	Secondary CPU processor version
--
[[qdm]]*+QDM+*::	Query device for model identification
+
--
.Reply
----
(AAA
----
.e.g.
----
(002
----

Where:

+AAA+::	Model identification.

For <<protocol,P16>> devices, model number, i.e. +AAA+, identifies <<mt,model type>> as follows:

[cols="20^,80"]
|====
|Value		|Corresponding type
|>= +200+	|<<self-use,Self-use (/Home solar)>>
|   +151+	|<<off-grid,Off-grid (/Stand alone)>> with <<vextex,grid relay disconnected in Inverter mode>> (Vextex)
|   +150+	|<<off-grid,Off-grid (/Stand alone)>> with grid relay connected in Inverter mode
|>= +100+	|<<grid-tie,Grid-tie>>
|>=  +50+	|<<grid-tie-with-backup,Grid-tie with backup (/Hybrid)>>
|====

For grid-connected models (i.e. all but +150+ and +151+), once you remove that signaling' number from the model number the remainder will identify the grid standard in use:

[cols="35^m,65"]
|====
|Remainder	|Grid standard
| 0		|VDE0126
| 1		|AS4777
| 2		|DK
| 3		|RD1663
| 4		|G83
| 6		|USH (240 V)
| 7		|USL (208 V)
| 8		|VDE4105
| 9		|Korea
|10		|Taiwan
|11		|Sweden
|====

.e.g.:
Model number: ::		+109+
Model type: ::			+109+ >= +100+	&&
				+109+ <  +200+	&&
				+109+ != +150+	&&
				+109+ != +151+
				-> Grid-tie
Grid standard in use: ::	+109+ - +100+ = +9+
			-> Korea
--
[[dm]]*+DMODEL<n>+*::	Set <<qdm,device model>> to *+<n>+* (3 digit integer, +NNN+) (<<protocol,P16>> only)
*+QID+*::		Query device for serial number
+
--
.Reply
----
(NNNNNNNNNNNNNNNNNNN
----
.e.g.
----
(0000000000000000000
----

Where:

+N+..+N+::	Device serial number (not fixed length)
--
*+QPIRI+*::		Query device for rated informations #1
+
--
.Reply
----
(AAA.A BB.B CCC.C DDD.D EEE.E FF.F GGG.G H II J
----
.e.g.
----
(230.0 50.0 013.0 230.0 013.0 18.0 048.0 1 10 0
----

Where:

[[qpiri-#1]]+AAA.A+::	Nominal grid-connected voltage (V)
[[qpiri-#2]]+BB.B+::	Nominal grid-connected frequency (Hz)
+CCC.C+::		Nominal grid-connected current (A)
+DDD.D+::		AC output rating voltage (V)
+EEE.E+::		AC output rating current (A)
+FF.F+::		Maximum input current for each PV (A)
+GGG.G+::		Battery rating voltage (V)
[[qpiri-#8]]+H+::	Number of MPP trackers
[[qpiri-#9]]+II+::	<<mt,Model type>>:
			- 00 -> <<grid-tie,Grid-tie>>
			- 01 -> <<off-grid,Off-grid (/Stand alone)>>
			- 10 -> <<grid-tie-with-backup,Grid-tie with backup (/Hybrid)>>
			- 11 -> <<self-use,Self-use (/Home solar)>>
+J+::			Device type:
			- 0 -> transformerless
			- 1 -> with transformer
--
[[v]]*+V<n>+*::		Set <<qpiri-#1,nominal voltage>> to *+<n>+* (3 digit integer, +NNN+) Volt (<<protocol,P16>> only)
[[f]]*+F<n>+*::		Set <<qpiri-#2,nominal frequency>> to *+<n>+* [+50+, +60+] Hertz (<<protocol,P16>> only)
*+PVN<n>+*::		Set <<qpiri-#8,number of MPP trackers in use>> to *+<n>+* [+01+..+99+]
*+QMD+*::		Query device for rated informations #2
+
--
.Reply
----
(AAAAAAAAAAAAAAA BBBBBBB CC D/E FFF GGG HH II.I
----
.e.g.
----
(###########PV3K ###3000 99 1/1 360 230 04 12.0
----

Where:

+AAAAAAAAAAAAAAA+::	Device model (15 characters, filled with spaces or +#+)
+BBBBBBB+::		Output rated power (W, 7 characters, filled with spaces or +#+)
+CC+::			Output power factor (%)
+D+::			Input phases
+E+::			Output phases
+FFF+::			Nominal input voltage (V)
+GGG+::			Nominal output voltage (V)
+HH+::			Number of batteries
+II.I+::		Nominal battery voltage (V)
--
*+I+*::			Query device for rated informations #3
+
--
.Reply
----
(DSP:AA-AA-AA,BB:BB MCU:CC-CC-CC,DD:DD
----
.e.g.
----
(DSP:14-03-03,14:30 MCU:14-01-15,17:20
----

Where:

+AA-AA-AA+::	DSP manufacturing date (in +YY-MM-DD+ format)
+BB:BB+::	DSP manufacturing time (in +hh:mm+ format)
+CC-CC-CC+::	MCU manufacturing date (in +YY-MM-DD+ format)
+DD:DD+::	MCU manufacturing date (in +hh:mm+ format)
--


[[default]]
Default values
~~~~~~~~~~~~~~

*+QDI+*::	Query device for <<reset-to-default,default>> values #1
+
--
.Reply
----
(AAA.A BBB.B CC.C DD.D EEE.E FFF.F GG.G HH.H III JJJ KKK LLL MMMMM NNN OO PP QQQ RR
----
.e.g.
----
(264.5 184.0 51.5 47.5 264.5 184.0 51.5 47.5 500 090 450 120 03000 253 02 04 --- --
----

Where:

+AAA.A+::	<<gov,Grid output high voltage>> (V)
+BBB.B+::	<<gov,Grid output low voltage>> (V)
+CC.C+::	<<gof,Grid output high frequency>> (Hz)
+DD.D+::	<<gof,Grid output low frequency>> (Hz)
+EEE.E+::	<<giv,Grid input high voltage>> (V)
+FFF.F+::	<<giv,Grid input low voltage>> (V)
+GG.G+::	<<gif,Grid input high frequency>> (Hz)
+HH.H+::	<<gif,Grid input low frequency>> (Hz)
+III+::		<<pviv,PV input high voltage>> (V)
+JJJ+::		<<pviv,PV input low voltage>> (V)
+KKK+::		<<mppv,MPP high voltage>> (V)
+LLL+::		<<mppv,MPP low voltage>> (V)
+MMMMM+::	<<mop,Maximum output power>> (W)
+NNN+::		<<giav,Max grid input average voltage>> (V)
+OO+::		<<lst,LCD sleep time>> (units of 30 seconds)
+PP+::		*{sp}unknown *
+QQQ+::		*{sp}unknown *
+RR+::		*{sp}unknown *
--
*+QDI2+*::	Query device for <<reset-to-default,default>> values #2
+
--
.Reply
----
(AA.A BB.B CCC DD.D EE.E FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
----
.e.g.
----
(25.0 54.0 060 42.0 56.0 --------------------------------------
----

Where:

+AA.A+::	<<bcd,Max battery-charging current>> (A)
+BB.B+::	<<bcd,Floating battery-charging voltage>> (V)
+CCC+::		<<gwt,Waiting time before grid connection>> (seconds)
+DD.D+::	<<bdl,Cut-off battery-discharging voltage>> (V)
+EE.E+::	<<bcd,Bulk battery-charging voltage>> (V)
+F+..+F+::	*{sp}unknown *
--


Limits
~~~~~~

*+QVFTR+*::	Query device for acceptable limits
+
--
.Reply
----
(AAA.A BBB.B CCC.C DDD.D EE.E FF.F GG.G HH.H III JJJ KK.K LL.L MM.M NN.N OOO PPP QQQ RRR SSS TTT UUU VVV WWWWW XXXXX YY.Y ZZ.Z @@
----
.e.g.
----
(276.0 235.0 225.0 180.0 55.0 50.1 49.9 45.0 070 005 58.0 48.0 25.0 00.5 500 450 200 090 450 400 200 110 03000 00000 58.0 50.0 --
----

Where:

+AAA.A+::	Max <<gov,grid output high voltage>> (V) *and* (<<protocol,P16>> only) max <<giv,grid input high voltage>> (V)
+BBB.B+::	Min <<gov,grid output high voltage>> (V) *and* (<<protocol,P16>> only) min <<giv,grid input high voltage>> (V)
+CCC.C+::	Max <<gov,grid output low voltage>> (V) *and* (<<protocol,P16>> only) max <<giv,grid input low voltage>> (V)
+DDD.D+::	Min <<gov,grid output low voltage>> (V) *and* (<<protocol,P16>> only) min <<giv,grid input low voltage>> (V)
+EE.E+::	Max <<gof,grid output high frequency>> (Hz) *and* (<<protocol,P16>> only) max <<gif,grid input high frequency>> (Hz)
+FF.F+::	Min <<gof,grid output high frequency>> (Hz) *and* (<<protocol,P16>> only) min <<gif,grid input high frequency>> (Hz)
+GG.G+::	Max <<gof,grid output low frequency>> (Hz) *and* (<<protocol,P16>> only) max <<gif,grid input low frequency>> (Hz)
+HH.H+::	Min <<gof,grid output low frequency>> (Hz) *and* (<<protocol,P16>> only) min <<gif,grid input low frequency>> (Hz)
+III+::		Max <<gwt,grid wait time>> (seconds)
+JJJ+::		Min <<gwt,grid wait time>> (seconds)
+KK.K+::	Max <<bcd,floating battery-charging voltage>> (V)
+LL.L+::	Min <<bcd,floating battery-charging voltage>> (V)
+MM.M+::	Max <<bcd,max battery-charging current>> (A)
+NN.N+::	Min <<bcd,max battery-charging current>> (A)
+OOO+::		Max <<pviv,PV input high voltage>> (V)
+PPP+::		Min <<pviv,PV input high voltage>> (V)
+QQQ+::		Max <<pviv,PV input low voltage>> (V)
+RRR+::		Min <<pviv,PV input low voltage>> (V)
+SSS+::		Max <<mppv,MPP high voltage>> (V)
+TTT+::		Min <<mppv,MPP high voltage>> (V)
+UUU+::		Max <<mppv,MPP low voltage>> (V)
+VVV+::		Min <<mppv,MPP low voltage>> (V)
+WWWWW+::	Max <<mop,maximum output power>> (W)
+XXXXX+::	Min <<mop,maximum output power>> (W)
+YY.Y+::	Max <<bcd,bulk battery-charging voltage>> (V)
+ZZ.Z+::	Min <<bcd,bulk battery-charging voltage>> (V)
+@@+::		*{sp}unknown *
--


Settings
~~~~~~~~


[[gov]]
Grid output voltage
^^^^^^^^^^^^^^^^^^^

*+QGOV+*::	Query device for grid output voltage limits
+
--
.Reply
----
(AAA.A BBB.B
----
.e.g.
----
(264.5 184.0
----

Where:

+AAA.A+::	Grid output high voltage (V)
+BBB.B+::	Grid output low voltage (V)
--
*+GOHV<n>+*::	Set grid output high voltage to *+<n>+* (4 digit decimal number, +NNN.N+) Volt
*+GOLV<n>+*::	Set grid output low voltage to *+<n>+* (4 digit decimal number, +NNN.N+) Volt


[[giv]]
Grid input voltage (<<protocol,P16>> only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*+QBYV+*::	Query device for grid input voltage limits
+
--
.Reply
----
(AAA.A BBB.B
----
.e.g.
----
(100.0 050.0
----

Where:

+AAA.A+::	Grid input high voltage (V)
+BBB.B+::	Grid input low voltage (V)
--
*+PHV<n>+*::	Set grid input high voltage to *+<n>+* (4 digit decimal number, +NNN.N+) Volt
*+PLV<n>+*::	Set grid input low voltage to *+<n>+* (4 digit decimal number, +NNN.N+) Volt


[[gof]]
Grid output voltage
^^^^^^^^^^^^^^^^^^^

*+QGOF+*::	Query device for grid output frequency limits
+
--
.Reply
----
(AA.A BB.B
----
.e.g.
----
(51.5 47.5
----

Where:

+AA.A+::	Grid output high frequency (Hz)
+BB.B+::	Grid output low frequency (Hz)
--
*+GOHF<n>+*::	Set grid output high frequency to *+<n>+* (3 digit decimal number, +NN.N+) Hertz
*+GOLF<n>+*::	Set grid output low frequency to *+<n>+* (3 digit decimal number, +NN.N+) Hertz


[[gif]]
Grid input voltage (<<protocol,P16>> only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*+QBYF+*::	Query device for grid input frequency limits
+
--
.Reply
----
(AA.A BB.B
----
.e.g.
----
(10.0 05.0
----

Where:

+AA.A+::	Grid input high frequency (Hz)
+BB.B+::	Grid input low frequency (Hz)
--
*+PGF<n>+*::	Set grid input high frequency to *+<n>+* (3 digit decimal number, +NN.N+) Hertz
*+PSF<n>+*::	Set grid input low frequency to *+<n>+* (3 digit decimal number, +NN.N+) Hertz


[[gwt]]
Grid wait time
^^^^^^^^^^^^^^

*+QFT+*::	Query device for waiting time before grid connection
+
--
.Reply
----
(AAA
----
.e.g.
----
(060
----

Where:

+AAA+::	Grid wait time (seconds)
--
*+FT<n>+*::	Set waiting time before grid connection to *+<n>+* (3 digit integer, +NNN+) seconds


[[bcd]]
Battery-charging data (<<protocol,P16>> only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*+QCHGS+*::		Query device for battery-charging data
+
--
.Reply
----
(AA.A BB.B CC.C DD.D
----
.e.g.
----
(00.3 54.0 25.0 55.4
----

Where:

+AA.A+::	Battery-charging current (A)
+BB.B+::	Floating battery-charging voltage (V)
+CC.C+::	Max battery-charging current (A)
+DD.D+::	Bulk battery-charging voltage (V)
--
*+MCHGV<n>+*::		Set floating battery-charging voltage to *+<n>+* (3 digit decimal number, +NN.N+) Volt
*+MCHGC<n>+*::		Set max battery-charging current to *+<n>+* (3 digit decimal number, +NN.N+) Ampère
*+BCHGV<n>+*::		Set bulk battery-charging voltage to *+<n>+* (3 digit decimal number, +NN.N+) Volt
*+QOFFC+*::		Query device for battery charger limits
+
--
.Reply
----
(AA.A BB.B CCC
----
.e.g.
----
(00.0 53.0 060
----

Where:

+AA.A+::	Min floating battery-charging current (A)
+BB.B+::	Restart battery-charging voltage (V)
+CCC+::		Period of time floating battery-charging current should stay below the above limit before switching off the charger (minutes)
--
*+OFFC<a> <b> <c>+*::	Set battery charger limits:
			- min floating battery-charging current to *+<a>+* (3 digit decimal number, +NN.N+) Ampère
			- restart battery-charging voltage to *+<b>+* (3 digit decimal number, +NN.N+) Volt
			- period of time floating battery-charging current should stay below the above limit before switching off the charger to *+<c>+* (3 digit integer, +NNN+) minutes


[[bdl]]
Battery-discharging limits (<<protocol,P16>> only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

*+QBSDV+*::		Query device for battery-discharging limits
+
--
.Reply
----
(AA.A BB.B CC.C DD.D
----
.e.g.
----
(48.0 48.0 48.0 49.4
----

Where:

+AA.A+::	Cut-off battery-discharging voltage when grid is unavailable (V)
+BB.B+::	Cut-off battery-discharging voltage when grid is available (V)
+CC.C+::	Restart battery-discharging voltage when grid is unavailable (V)
+DD.D+::	Restart battery-discharging voltage when grid is available (V)
--
*+BSDV<a> <b>+*::	Set cut-off battery-discharging voltage:
			- when grid is unavailable to *+<a>+* (3 digit decimal number, +NN.N+) Volt
			- when grid is available to *+<b>+* (3 digit decimal number, +NN.N+) Volt
*+DSUBV<a> <b>+*::	Set restart battery-discharging voltage:
			- when grid is unavailable to *+<a>+* (3 digit decimal number, +NN.N+) Volt
			- when grid is available to *+<b>+* (3 digit decimal number, +NN.N+) Volt


[[pviv]]
PV input voltage
^^^^^^^^^^^^^^^^

*+QPVIPV+*::	Query device for PV input voltage limits
+
--
.Reply
----
(AAA BBB
----
.e.g.
----
(500 090
----

Where:

+AAA+::	PV input high voltage (V)
+BBB+::	PV input low voltage (V)
--
*+PVIPHV<n>+*::	Set PV input high voltage to *+<n>+* (3 digit integer, +NNN+) Volt
*+PVIPLV<n>+*::	Set PV input low voltage to *+<n>+* (3 digit integer, +NNN+) Volt


[[mppv]]
MPP voltages
^^^^^^^^^^^^

*+QMPPTV+*::	Query device for MPP voltage limits
+
--
.Reply
----
(AAA BBB
----
.e.g.
----
(450 120
----

Where:

+AAA+::	MPP high voltage (V)
+BBB+::	MPP low voltage (V)
--
*+MPPTHV<n>+*::	Set MPP high voltage to *+<n>+* (3 digit integer, +NNN+) Volt
*+MPPTLV<n>+*::	Set MPP low voltage to *+<n>+* (3 digit integer, +NNN+) Volt


[[mop]]
Maximum output power
^^^^^^^^^^^^^^^^^^^^

*+QOPMP+*::	Query device for maximum output power
+
--
.Reply
----
(AAAAA
----
.e.g.
----
(03000
----

Where:

+AAAAA+::	Maximum output power (W)
--
*+OPMP<n>+*::	Set maximum output power to *+<n>+* (5 digit integer, +NNNNN+, roundend to tens) Watt


[[mgp]]
Maximum power feeding grid
^^^^^^^^^^^^^^^^^^^^^^^^^^

*+QGPMP+*::	Query device for maximum power feeding grid
+
--
.Reply
----
(AAAAA
----
.e.g.
----
(03000
----

Where:

+AAAAA+::	Maximum power feeding grid (W)
--
*+GPMP<n>+*::	Set maximum power feeding grid to *+<n>+* (5 digit integer, +NNNNN+, rounded to tens) Watt


[[lst]]
LCD sleep time
^^^^^^^^^^^^^^

*+QLST+*::	Query device for LCD sleep time (time after which LCD screen-saver starts)
+
--
.Reply
----
(AA
----
.e.g.
----
(10
----

Where:

+AA+::	LCD sleep time (seconds)
--
*+LST<n>+*::	Set LCD sleep time (time after which LCD screen-saver starts) to *+<n>+* [+00+..+99+] units of 30 seconds


Allowed charging time (<<protocol,P16>> only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*+QCHT+*::		Query device for allowed charging time settings
+
--
.Reply
----
(AAAA BBBB
----
.e.g.
----
(1215 2130
----

Where:

+AAAA+::	Start time (in +hhmm+ format) of the allowed charging period
+BBBB+::	End time (in +hhmm+ format) of the allowed charging period
--
*+CHTH<time>+*::	Set start time of the allowed charging period to *+<time>+* (in +hhmm+ format)
*+CHTL<time>+*::	Set end time of the allowed charging period to *+<time>+* (in +hhmm+ format)

NOTE:	Setting both times to +0000+ makes the charger operate all time.


[[ct]]
Allowed charging-from-AC time (<<protocol,P16>> only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*+QPKT+*::		Query device for allowed charging-from-AC time settings
+
--
.Reply
----
(AAAA BBBB
----
.e.g.
----
(1215 2130
----

Where:

+AAAA+::	Start time (in +hhmm+ format) of the allowed charging-from-AC period
+BBBB+::	End time (in +hhmm+ format) of the allowed charging-from-AC period
--
*+PKT<a> <b>+*::	Set allowed charging-from-AC period:
			- start time to *+<a>+* (in +hhmm+ format)
			- end time to *+<b>+* (in +hhmm+ format)

NOTE:	Setting both times to +0000+ makes AC charger operate all time.


Allowed AC-output time (<<protocol,P16>> only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*+QLDT+*::		Query device for allowed AC-output time settings
+
--
.Reply
----
(AAAA BBBB
----
.e.g.
----
(1215 2130
----

Where:

+AAAA+::	Start time (in +hhmm+ format) of the allowed AC-output period
+BBBB+::	End time (in +hhmm+ format) of the allowed AC-output period
--
*+LDT<a> <b>+*::	Set allowed AC-output period:
			- start time to *+<a>+* (in +hhmm+ format)
			- end time to *+<b>+* (in +hhmm+ format)

NOTE:	Setting both times to +0000+ disables the timer.


[[giav]]
Grid input average voltage
^^^^^^^^^^^^^^^^^^^^^^^^^^

*+QGLTV+*::	Query device for grid input average voltages limits
+
--
.Reply
----
(AAA BBB
----
.e.g.
----
(253 ---
----

Where:

+AAA+::	Max grid input average voltage (V)
+BBB+::	Min grid input average voltage (V)
--
*+GLTHV<n>+*::	Set max grid input average voltage to *+<n>+* (3 digit integer, +NNN+) Volt


Output power factor (<<protocol,P15>> only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*+QOPF+*::	Query device for output power factor
+
--
.Reply
----
(AAA
----
.e.g.
----
(100
----

Where:

+AAA+::	Output power factor (%)
--
*+SOPF<n>+*::	Set output power factor to *+<n>+* [+-099+..+-090+; `+090`..`+100`] %


Power percent setting (<<protocol,P15>> only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*+QPPS+*::	Query device for power percent settings
+
--
.Reply
----
(AAA
----
.e.g.
----
(100
----

Where:

+AAA+::	Power percent setting (%)
--
*+PPS<n>+*::	Set power percent setting to *+<n>+* [+010+..+100+] %


Power factor percent (<<protocol,P15>> only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*+QPPD+*::	Query device for power factor percent
+
--
.Reply
----
(AAA
----
.e.g.
----
(100
----

Where:

+AAA+::	Power factor percent (%)
--
*+PPD<n>+*::	Set power factor percent to *+<n>+* [+050+..+100+] %


Power factor curve (<<protocol,P15>> only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*+QPDG+*::	Query device for power factor curve capability
+
--
.Reply
----
(A
----
.e.g.
----
(1
----

Where:

+A+::	Power factor curve capability:
	- +0+ -> disabled
	- +1+ -> enabled
--
*+PDG<n>+*::	Enable (*+<n>+*: +1+) or disable (*+<n>+*: +0+) power factor curve capability
*+QPFL+*::	Query device for minimum value of power factor curve
+
--
.Reply
----
(AAA
----
.e.g.
----
(100
----

Where:

+AAA+::	Minimum value of power factor curve (%)
--
*+PFL<n>+*::	Set minimum value of power factor curve to *+<n>+* [+-99+..+-90+ but without the sign, so: +099+..+090+] %


Device date/time
^^^^^^^^^^^^^^^^

*+QT+*::		Query device for date/time
+
--
.Reply
----
(AAAAAAAABBBBBB
----
.e.g.
----
(20140115121521
----

Where:

+AAAAAAAA+::	Device date (in +YYYYMMDD+ format)
+BBBBBB+::	Device time (in +hhmmss+ format)
--
*+DAT<date><time>+*::	Set device date to *+<date>+* (in +YYMMDD+ format) *and* time to *+<time>+* (in +hhmmss+ format)


Produced energy
~~~~~~~~~~~~~~~

*+QFET+*::				Query device for energy start date
+
--
.Reply
----
(AAAAAAAABB
----
.e.g.
----
(2013121502
----

Where:

+AAAAAAAA+::	Energy start date (in +YYYYMMDD+ format)
+BB+::		Energy start time (in +hh+ format)
--
*+QEH<date><hour><checksum>+*::		Query device for energy produced in the specific hour *+<hour>+* (in +hh+ format) at date *+<date>+* (in +YYYYMMDD+ format).
					*+<checksum>+* is 0-padded to 3 bytes length.
+
--
.Reply
----
(AAAAA
----
.e.g.
----
(00004
----

Where:

+AAAAA+::	Energy produced in the specific hour *+<hour>+* at date *+<date>+* (Wh)
--
```
```
*+QED<date><checksum>+*::		Query device for energy produced in the specific day at date *+<date>+* (in +YYYYMMDD+ format).
					*+<checksum>+* is 0-padded to 3 bytes length.
+
--
.Reply
----
(AAAAAA
----
.e.g.
----
(005758
----

Where:

+AAAAAA+::	Energy produced in the specific day at date *+<date>+* (Wh)
--
*+QEM<year><month><checksum>+*::	Query device for energy produced in the specific month *+<month>+* (in +MM+ format) of year *+<year>+* (in +YYYY+ format).
					*+<checksum>+* is 0-padded to 3 bytes length.
+
--
.Reply
----
(AAAAAAA
----
.e.g.
----
(0000000
----

Where:

+AAAAAAA+::	Energy produced in the specific month *+<month>+* in year *+<year>+* (Wh)
--
*+QEY<year><checksum>+*::		Query device for energy produced in the specific year *+<year>+* (in +YYYY+ format).
					*+<checksum>+* is 0-padded to 3 bytes length.
+
--
.Reply
----
(AAAAAAAA
----
.e.g.
----
(00000000
----

Where:

+AAAAAAAA+::	Energy produced in the specific year *+<year>+* (Wh)
--


Device tests
~~~~~~~~~~~~

*+ST+*::	Start a grid self test
*+QSTS+*::	Query device for self test results
+
--
.Reply
----
(AA BBB CCC DDD EEE FFF GGG HHH III
----
.e.g.
----
(01 001 002 003 004 005 006 007 008
----

Where:

+AA+::	Self test result:
	- +00+ -> still self testing
	- +01+ -> self test passed
	- other values -> self test failed
+BBB+::	High voltage [threshold: nominal voltage * 1.2 (230 V * 1.2 = 276 V)] (V)
+CCC+::	Low voltage [threshold: nominal voltage * 0.8 (230 V * 0.8 = 184 V)] (V)
+DDD+::	High frequency [threshold: nominal frequency + 0.3 (50 + 0.3 = 50.3 Hz)] (Hz)
+EEE+::	Low frequency [threshold: nominal frequency - 0.3 (50 - 0.3 = 49.7 Hz)] (Hz)
+FFF+::	High voltage trip time [threshold: 100 ms] (ms)
+GGG+::	Low voltage trip time [threshold: 100 ms] (ms)
+HHH+::	High frequency trip time [threshold: 100 ms] (ms)
+III+::	Low frequency trip time [threshold: 100 ms] (ms)
--


Device management
~~~~~~~~~~~~~~~~~

*+SOFF+*::	Turn off AC output
*+SON+*::	Turn on AC output
*+FGD+*::	Disconnect grid
*+FGE+*::	Connect grid
*+GTS<n>+*::	Put device on (*+<n>+*: +1+) or out of (*+<n>+*: +0+) standby
*+OEEPB+*::	Executed before each <<dm,*+DMODEL<n>+*>>, <<v,*+V<n>+*>> and <<f,*+F<n>+*>> command


[[warnings]]
Warnings
--------

[cols="5>,90,5^",align="center"]
|====
|#	|Corresponding Warning							|Level
| 0	|[[device-fault]]Device has fault					|/
| 1	|CPU is performing the auto-correction of AD signals			|3
| 2	|An external Flash device failed					|1
| 3	|Input PV is found lost							|2
| 4	|PV input voltage reads low						|2
| 5	|Power island								|2
| 6	|An Error occurred in the CPU initialization				|1
| 7	|Power grid voltage exceeds the upper threshold				|2
| 8	|Power grid voltage falls below the lower threshold			|2
| 9	|Power grid frequency exceeds the upper threshold			|2
|10	|Power grid frequency falls below the lower threshold			|2
|11	|Power grid-connected average voltage exceeds the maximum threshold	|2
|12	|Require power from the power grid					|2
|13	|Emergent grid disconnection						|2
|14	|Battery voltage is too low						|2
|15	|Low battery								|2
|16	|Battery disconnected							|2
|17	|End of batter discharge						|2
|18	|Overload								|2
|19	|EPO active								|2
|22	|Over temperature alarm							|2
|23	|No electrical ground							|2
|24	|Fan fault								|2
|====


[[faults]]
Faults
------

[cols="5>m,90,5^",align="center"]
|====
|#	|Correspondig Fault								|Level
|01	|DC bus voltage exceeds the upper threshold					|1
|02	|DC bus voltage falls below the lower threshold					|1
|03	|DC bust voltage soft-start is time-out						|1
|04	|Inverter soft-start is time-out						|1
|05	|An Inverter overcurrent event is detected					|1
|06	|Over temperature fault								|1
|07	|An relay failure event is detected						|1
|08	|DC component in the output current exceeds the upper threshold			|1
|09	|PV input voltage exceeds the upper threshold					|1
|10	|Auxiliary power failed								|1
|11	|An PV input overcurrent event is detected					|1
|12	|Leakage current exceeds the allowable range					|1
|13	|PV insulation resistance is too low						|1
|14	|Inverter DC component exceeds the allowable range				|1
|15	|A difference occurred in the readings from the main and secondary controllers	|1
|16	|Leakage current CT failed							|1
|17	|Communication with the main and secondary controllers is interrupted		|1
|18	|An communicating error occurred in the handshake between MCU and DSP		|1
|19	|No electrical ground								|1
|20	|Discharge circuit fault							|1
|21	|Soft start in battery discharge fails						|1
|22	|Charging voltage is too high							|1
|23	|Overload fault									|1
|24	|Battery disconnected								|1
|25	|Inverter current is too high for a long time					|1
|26	|Short circuited on inverter output						|1
|27	|Fan fault									|1
|28	|OP Current Sensor fault							|1
|29	|Charger failure								|1
|30	|Version mismatch between controller board and power board			|1
|31	|Reverse connection of input and output wires					|1
|====


Operational modes
-----------------

[labeled]
[[bypass-mode]]			*Bypass Mode*::
	Bypass voltage to output.
[[bypass-wo-chrg-mode]]		*Bypass without charging Mode*::
	Bypass voltage to output without charging battery.
[[bypass-w-pvchrg-mode]]	*Bypass with PV charging Mode*::
	If PV power is sufficient, it will charge the battery and AC power will provide power to load.
[[bypass-w-acchrg-mode]]	*Bypass with AC charging Mode*::
	If PV power is insufficient, AC power will charge the battery and provide power to load.
[[fault-mode]]			*Fault Mode*::
	The device is in Fault Mode'' when a fault is found.
[[grid-mode]]			*Grid Mode*::
	The device is successfully connected to the grid.
[[grid-tie-w-backup-mode]]	*Grid-tie with backup Mode*::
	There are three power sources in Grid-tie with backup Mode'': PV power, battery power and utility power.
[[inverter-mode]]		*Inverter (Battery) Mode*::
	Utility power is not available or not connected.
	Possible power flows:
	1. If PV power is not available, battery power will provide power to the load.
	2. If PV power is available and sufficient, PV power will charge battery and provide power to load.
	3. If PV power is not sufficient, PV power and battery power will provide power to the load at the same time.
[[line-mode]]			*Line Mode*::
	Utility power exists or is available during this mode.
	Possible power flows:
	1. If PV power and battery energy are not available, utility will provide power to loads directly.
	2. If only utility power exists, it will charge battery and provide power to the load.
	3. If only PV power exists without battery connected, it will provide power the load.
	   If there is remaining power, it will feed-in to the grid.
	4. If PV power is sufficient but battery power is insufficient, PV power will charge the battery, provide power to the load and feed in to the grid.
	5. If PV power is weak, utility exists and battery power is insufficient, PV power and utility power will charge battery at the same time.
	   Besides, utility power will provide power to the load.
[[power-on-mode]]		*Power On Mode*::
	Device is going on.
[[shutdown-mode]]		*Shutdown Mode*::
	Device is shutting down.
[[standby-mode]]		*Standby Mode*::
	Only PV power is available.
	There is no load connection and no utility and battery power available during this mode.
[[standby-wo-chrg-mode]]	*Standby without charging Mode*::
	No output and no battery charging.
[[standby-w-pvchrg-mode]]	*Standby with PV charging Mode*::
	PV power will charge the battery.
[[standby-w-acchrg-mode]]	*Standby with AC charging Mode*::
	AC power will charge the battery.


[[mt]]
Model type
----------

[[grid-tie]]
Grid-tie [<<qpiri-#9,type: +00+>>]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PV power only feeds-in to the grid.
No priority setting is available (i.e. <<priority,priority: *+00+*>>).

[NOTE]
====
For the sake of coherence, when this type is chosen:

- <<oops-c,Allow to feed-in to the grid>>'' option is always enabled, i.e. always feed-in to the grid;
- <<oops-a,Allow PV to charge battery>>'', <<oops-b,Allow AC to charge battery>>'', <<oops-d,Allow battery to discharge when PV is available>>'', <<oops-e,Allow battery to discharge when PV is unavailable>>'', <<oops-f,Allow battery to feed-in to the grid when PV is available>>'' and <<oops-g,Allow battery to feed-in to the grid when PV is unavailable>>'' options are always disabled, i.e. ignore battery (if any).
====


[[off-grid]]
Off-grid (/Stand alone) [<<qpiri-#9,type: +01+>>]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PV power only provides power to the load and charge battery.
Feed-in to the grid is not allowed.

[labeled]
<<priority,Priority: *+01+*>>::
	*PV energy supply priority setting*: 1. Battery, 2. Load.
	- PV power will charge battery first.
	- After battery is fully charged, if there is remaining PV power left, it will provide power to the load.
	- At the same time, *the grid relay is connected in inverter mode*.
	  That means the transfer time from inverter mode to battery mode will be less than 15ms.
	  Besides, it will avoid overload fault because grid can supply load when connected load is over 3KW.
+
--
NOTE:	When this type and priority are chosen, for the sake of coherence, <<oops-d,Allow battery to discharge when PV is available>>'' option is always disabled, i.e. don't take from battery when PV is available.
--
<<priority,Priority: *+02+*>> *and* <<qdm,model>> is *+150+*::
	*PV energy supply priority setting*: 1. Load, 2. Battery.
	- PV power will provide power to the load first and then charge battery.
	- At the same time, *the grid relay is connected in inverter mode*.
	  That means the transfer time from inverter mode to battery mode will be less than 15ms.
	  Besides, it will avoid overload fault because grid can supply load when connected load is over 3KW.
[[vextex]]<<priority,Priority: *+02+*>> *and* <<qdm,model>> is *+151+*::
	*PV energy supply priority setting*: 1. Load, 2. Battery.
	- PV power will provide power to the load first and then charge battery.
	- *The grid relay is NOT connected in inverter mode*.
	  That means the transfer time from inverter mode to battery mode will be about 15ms.
	  If connected load is over 3KW, this inverter will activate fault protection.
+
--
NOTE:	When this type and priority are chosen, for the sake of coherence, <<oops-d,Allow battery to discharge when PV is available>>'' option is always enabled, i.e. take from battery when PV is available.
--

*Battery charging source* and *load supply source* can be personalized <<oops,setting the appropriate operational options>>.


NOTE:	When this type is chosen, for the sake of coherence, <<oops-c,Allow to feed-in to the grid>>'', <<oops-f,Allow battery to feed-in to the grid when PV is available>>'' and <<oops-g,Allow battery to feed-in to the grid when PV is unavailable>>'' options are always disabled, i.e. don't feed-in to grid.


[[grid-tie-with-backup]]
Grid-tie with backup (/Hybrid) [<<qpiri-#9,type: +10+>>]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PV power can feed-in back to grid, provide power to the load and charge battery.

[labeled]
<<priority,Priority: *+01+*>>::
	*PV energy supply priority setting*: 1. Battery, 2. Load, 3. Grid.
	- PV power will charge battery first, then provide power to the load.
	- If there is any remaining power left, it will feed-in to the grid (if <<oops-c,Allow to feed-in to the grid>>'' option is enabled).
+
--
NOTE:	When this type and priority are chosen, for the sake of coherence, <<oops-d,Allow battery to discharge when PV is available>>'' and <<oops-f,Allow battery to feed-in to the grid when PV is available>>'' options are always disabled, i.e. don't take from battery when PV is available.
--
<<priority,Priority: *+02+*>>::
	*PV energy supply priority setting*: 1. Load, 2. Battery, 3. Grid.
	- PV power will provide power to the load first, then it will charge battery.
	- If there is any remaining power left, it will feed-in to the grid (if <<oops-c,Allow to feed-in to the grid>>'' option is enabled).
<<priority,Priority: *+03+*>>::
	*PV energy supply priority setting*: 1. Load, 2. Grid, 3. Battery.
	- PV power will provide power to the load first.
	- If there is more PV power available, it will feed-in to the grid (if <<oops-c,Allow to feed-in to the grid>>'' option is enabled).
	- If feed-in power reaches <<mgp,maximum power feeding grid'' setting>>, the remaining power will charge battery.

*Battery charging source* and *load supply source* can be personalized <<oops,setting the appropriate operational options>>.


[[self-use]]
Self-use (/Home solar) [<<qpiri-#9,type: +11+>>]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The inverter is only operated between two working logics based on defined <<ct,peak time (i.e. when grid doesn't charge battery)>> and <<ct,off-peak time (i.e. when grid charges battery)>> of electricity and <<mgp,off-peak electricity>> demand.
No priority setting is available (i.e. <<priority,priority: *+00+*>>).

[labeled]
Working logic under peak time::
+
--
*PV energy supply priority*: 1. Load, 2. Battery, 3. Grid.

- PV power will provide power to the load first.
- If PV power is sufficient, it will charge battery next.
- If there is remaining PV power left, it will feed-in to the grid (if <<oops-c,Allow to feed-in to the grid>>'' option is enabled).

*Battery charging source*: PV only.

- Only after PV power fully supports the load, the remaining PV power is allowed to charge battery during peak time.

*Load supply source*: 1. PV, 2. Battery, 3. Grid.

- PV power will provide power to the load first.
- If PV power is not sufficient, battery power will back up the load.
- If battery power is not available, grid will provide the load.
- When PV power is not available, battery power will supply the load first.
- If battery power is running out, grid will back up the load.
--
Working logic under off-peak time::
+
--
*PV energy supply priority*: 1. Load, 2. Grid, 3. Battery.

- PV power will provide power to the load first.
- If PV power is sufficient, it will feed-in to the grid (if <<oops-c,Allow to feed-in to the grid>>'' option is enabled).
- Only after feed-in power reaches <<mgp,maximum power feeding grid'' setting>>, the remaining PV power will charge battery.

*Battery charging source*: PV and grid charge battery.

- PV power will charge battery first during off-peak time.
- If it’s not sufficient, grid will charge battery.

*Load supply source*: 1. PV, 2. Grid, 3. Battery.

- When battery is fully charged, remaining PV power will provide power to the load first.
- If PV power is not sufficient, grid will back up the load.
- If grid power is not available, battery power will provide power to the load.
--

[NOTE]
====
For the sake of coherence, when this type is chosen:

- <<oops-a,Allow PV to charge battery>>'' and <<oops-b,Allow AC to charge battery>>'' options are always enabled, i.e. always allow to charge battery;
- <<oops-d,Allow battery to discharge when PV is available>>'', <<oops-e,Allow battery to discharge when PV is unavailable>>'', <<oops-f,Allow battery to feed-in to the grid when PV is available>>'' and <<oops-g,Allow battery to feed-in to the grid when PV is unavailable>>'' options are always disabled.
====


Revision History
----------------

[cols="1^.^,2^.^,5.^,2.^",align="center"]
|====
|Rev.	|Date		|Description						|Author
|1.0	|02/2014	|Initial release					|Daniele Pezzini
|1.1	|06/2015	|Update some commands/queries with real device data	|Daniele Pezzini
|1.2	|07/2015	|Update some commands/queries with real device data	|Daniele Pezzini
|====
```

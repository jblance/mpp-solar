# PI30 Q1 definition #
from [AEVA Forums](https://forums.aeva.asn.au/viewtopic.php?title=pip4048ms-inverter&p=60229&t=4332#p60229)

##
```
(        All command responses start with the open parenthesis character.
0 AAAAA    Local inverter status (first field). This seems to be a bit field,
         commonly taking the values 0x3809 or similar (shows as 14345 decimal).
         Edit: this seems to become a count in seconds till the end of CV
         (absorb) charging, in firmware version 72.70.
 1 BBBBB    ParaExistInfo first field. This always seems to be 00001, even with
            no parallel card installed.
            Edit: this seems to become a count in seconds till the end of float
            charging (when it will start CC (bulk) charging), in firmware version
            72.70.
 2 CC       SccOkFlag. I assume that 1 means the SCC is powered and is
            communicating.
 3 DD       AllowSccOnFlag.
 4 EE       ChargeAverageCurrent. I'm not clear on what chargers are included.
 5 FFF      SCC PWM temperature, in °C. From global variable wSccPWMTemp.
 6 GGG      Inverter temperature, in °C. Presumed to be from the AC heatsink.
 7 HHH      "Battery temperature". It seems that this must be the temperature
            reported by a sensor on the battery to bus inverter heatsink.
 8 III      Transformer temperature. It's the result of calling _wTempDegreeTxt().
            Presumably also in °C.
 9 JJ       Parallel mode: 0 1 2 mean NEw, SLave, MAster.
10 KK       FanLockStatus. I'd say 01 means fans are locked, 00 means not locked.
11 LLL      FanPWMDuty. No longer used. Always 000.
12 MMMM     "FanPWM", but is actually speed in percent. 0000 represents off, and
            0100 represents 100% duty cycle (flat out). However, on start-up, this
            value goes to 0100 without the fans roaring. 0030 (30%) seems to be
            the lowest speed, quite quiet. At 42% load, the fans went to 42% 
            speed.
13 NNNN     SCC charge power, watts. This is one of the changes to firmware
            version 72.40 that is not present in version 52.30. In 72.40, the
            result of the call to _swGetSccChgPower() is divided by 10; in 52.30
            is is displayed as is. I suspect 52.30 would have displayed tenths of
            watts.
14 OOOO     ParaWarning. Presumably, some warning bitfield related to paralleled
            units.
15 PP.PP    SYNFreq. Wild guess: frequency of inverter after synchronising with
            the mains input.
16 QQ       Inverter charge status. This will likely be 10 for no charging, 11 for
            bulk stage, 12 for absorb, or 13 for float. However, bulk stage will
            usually report as 12, same as absorb. I don't know what the signif-
            icance of the leading "1" digit is; I've always found it to be one, but
            the firmware calculates this value modulo 10 (stripping off the tens
            digit) a lot of the time.
```
Edit March 2020: Firmware version 74.40 (which is for PF1 non-64V models) has an extra 10 fields, most concerning the equalisation settings. 

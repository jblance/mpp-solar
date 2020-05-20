#!/usr/bin/python3
#
#
# mpp_info_pub.py
#
# script to query MPP Solar PIP-4048MS inverter/charger
# - inverter connected to computer via serial
#      (USB to Serial converter used for testing)
# - posts results to MQTT broker
# - uses mpputils.py / mppcommands.py to abstract PIP communications
#
import paho.mqtt.publish as publish


from .mpputils import mppUtils
grab_settings = False


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='MPP Solar Inverter Info Utility')
    parser.add_argument('-s', '--grabsettings', action='store_true', help='Also get the inverter settings')
    parser.add_argument('-t', '--getstatus', action='store_true', help='Use the getstatus "helper"')
    parser.add_argument('-c', '--command', type=str, help='Command to execute [comma separated]', default=None)
    parser.add_argument('-d', '--device', type=str, help='Serial device(s) to communicate with [comma separated]', default='/dev/ttyUSB0')
    parser.add_argument('-M', '--model', type=str, help='Specifies the inverter model to select commands for, defaults to "standard", currently supports LV5048', default='standard')
    parser.add_argument('-b', '--baud', type=int, help='Baud rate for serial communications', default=2400)
    parser.add_argument('-q', '--broker', type=str, help='MQTT Broker hostname', default='mqtt_broker')
    parser.add_argument('-i', '--influx', action='store_true', help='Use Influx Line Protocol for the messgae format')
    parser.add_argument('-I', '--influx2', action='store_true', help='Use Influx Line Protocol II for the messgae format')
    parser.add_argument('--tag', type=str, help='Influx tag to use for all commands in this execution', default=None)
    args = parser.parse_args()

    # Process / loop through all supplied devices
    for usb_port in args.device.split(','):
        mp = mppUtils(usb_port, args.baud, args.model)
        serial_number = mp.getSerialNumber()

        # Collect Inverter Settings and publish
        if args.grabsettings:
            msgs = []
            settings = mp.getSettings()

            for setting in settings:
                for i in ['value', 'default', 'unit']:
                    topic = '{}/settings/{}/{}'.format(serial_number, setting, i)
                    msg = {'topic': topic, 'payload': '{}'.format(settings[setting][i])}
                    msgs.append(msg)
            # publish.multiple(msgs, hostname=args.broker)
            print(msgs)
            print(args.broker)

        if args.command:
            if args.influx:
                for _command in args.command.split(','):
                    msgs = []
                    _data = mp.getInfluxLineProtocol(_command)
                    for _item in _data:
                        # print(_item)
                        # _item = setting=total_ac_output_apparent_power value=1577.0,unit="VA"
                        # weather,location=us-midwest temperature=82 1465839830100400200
                        # |    -------------------- --------------  |
                        # |             |             |             |
                        # |             |             |             |
                        # +-----------+--------+-+---------+-+---------+
                        # |measurement|,tag_set| |field_set| |timestamp|
                        # +-----------+--------+-+---------+-+---------+
                        if args.tag:
                            tag = args.tag
                        else:
                            tag = _command
                        payload = '{},{}'.format(tag, _item)
                        msg = {'topic': tag, 'payload': payload}
                        msgs.append(msg)
                    publish.multiple(msgs, hostname=args.broker)
            elif args.influx2:
                for _command in args.command.split(','):
                    msgs = []
                    _data = mp.getInfluxLineProtocol2(_command)
                    if args.tag:
                        tag = args.tag
                    else:
                        tag = _command
                    for _item in _data:
                        # print(_item)
                        # _item = setting=total_ac_output_apparent_power value=1577.0,unit="VA"
                        # weather,location=us-midwest temperature=82 1465839830100400200
                        # |    -------------------- --------------  |
                        # |             |             |             |
                        # |             |             |             |
                        # +-----------+--------+-+---------+-+---------+
                        # |measurement|,tag_set| |field_set| |timestamp|
                        # +-----------+--------+-+---------+-+---------+
                        payload = 'mpp-solar,command={} {}'.format(tag, _item)
                        msg = {'topic': 'mpp-solar', 'payload': payload}
                        msgs.append(msg)
                    publish.multiple(msgs, hostname=args.broker)
            else:
                for _command in args.command.split(','):
                    msgs = []
                    _data = mp.getResponseDict(_command)
                    # {'serial_number': [u'9293333010501', u'']}
                    for _item in _data:
                        # 92931509101901/status/total_output_active_power/value 1250
                        # 92931509101901/status/total_output_active_power/unit W
                        # topic = '{}/status/{}/value'.format(serial_number, _item)
                        topic = '{}/{}/value'.format(_command, _item)
                        msg = {'topic': topic, 'payload': '{}'.format(_data[_item][0])}
                        msgs.append(msg)
                        topic = '{}/{}/unit'.format(_command, _item)
                        msg = {'topic': topic, 'payload': '{}'.format(_data[_item][1])}
                        msgs.append(msg)
                    publish.multiple(msgs, hostname=args.broker)
        # Collect Inverter Status data and publish
        if args.getstatus:
            msgs = []
            status_data = mp.getFullStatus()
            for status_line in status_data:
                for i in ['value', 'unit']:
                    # 92931509101901/status/total_output_active_power/value 1250
                    # 92931509101901/status/total_output_active_power/unit W
                    topic = '{}/status/{}/{}'.format(serial_number, status_line, i)
                    msg = {'topic': topic, 'payload': '{}'.format(status_data[status_line][i])}
                    msgs.append(msg)
            publish.multiple(msgs, hostname=args.broker)

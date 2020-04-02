#!/usr/bin/python
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
            for _command in args.command.split(','):
                msgs = []
                _data = mp.getResponseDict(_command)
                # {'serial_number': [u'9293333010501', u'']}
                for _item in _data:
                        # 92931509101901/status/total_output_active_power/value 1250
                        # 92931509101901/status/total_output_active_power/unit W
                        #topic = '{}/status/{}/value'.format(serial_number, _item)
                        topic = '{}/{}/value'.format(_command, _item)
                        msg = {'topic': topic, 'payload': '{}'.format(_data[_item][0])}
                        msgs.append(msg)
                        topic = '{}/status/{}/unit'.format(serial_number, _item)
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
            # print(msgs)
            # print(args.broker)
            # print(status_data)

# Adafruit IO has:
#    Battery Capacity (as %)         inverter-one-battery-capacity-percent
#    Output Power (W)                inverter-one-total-output-active-power-w
#    Fault Code (text text)          fault-code
#    Battery Voltage                 inverter-one-battery-voltage-v
#    Inverter Charge Status (text)   inverter-charge-status
#    Total Charging Current (A)      inverter-one-total-charging-current-a
#    Inverter 1 charging current (A) inverter-one-battery-charging-current-a
#    Inverter 2 charging current (A) inverter-two-battery-charging-current-a
#    Load (as %)                     inverter-one-load-percentage-percent

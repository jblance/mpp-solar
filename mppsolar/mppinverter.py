"""
MPP Solar Inverter Command Library
reference library of serial commands (and responses) for PIP-4048MS inverters
mppinverter.py
"""

import sys
if not sys.platform == 'esp32':
    import serial
    import os
else:
    from machine import UART

import time
import re
import logging
import json
import glob
from os import path

from .all_commands import commands

# from builtins import bytes

from .mppcommand import mppCommand

log = logging.getLogger('MPP-Solar')


class MppSolarError(Exception):
    pass


class NoDeviceError(MppSolarError):
    pass


class NoTestResponseDefined(MppSolarError):
    pass


def getDataValue(data, key):
    """
    Get value from data dict (loaded from JSON) or return empty String
    """
    if key == 'regex':
        if 'regex' in data and data['regex']:
            return re.compile(data['regex'])
        else:
            return None
    if key in data:
        return data[key]
    else:
        return ""


def isInverterSupported(inverter_model, json):
    """
    Determine if the command loaded from json supports the supplied inverter
    """
    supports = getDataValue(json, 'supports')
    nosupports = getDataValue(json, 'nosupports')
    log.debug("-----No supports {}".format(nosupports))
    # Some commands are specifically not supported by some models
    if inverter_model in nosupports:
        log.debug("Command {} not supported on inverter {}".format(getDataValue(json, 'name'), inverter_model))
        return False
    # JSON command support all inverters unless specified
    if supports == "":
        log.debug("Command {} supported all inverters".format(getDataValue(json, 'name')))
        return True
    elif inverter_model in supports:
        log.debug("Command {} supported by model {}".format(getDataValue(json, 'name'), inverter_model))
        return True
    else:
        return False


def getCommands(inverter_model):
    """
    Read in all the json files in the commands subdirectory
    this builds a list of all valid commands
    """
    log.info("Loading commands for inverter model: {}".format(inverter_model))
    COMMANDS = []
#    here = path.abspath(path.dirname(__file__))
#    files = glob.glob(here + '/commands/*.json')
    if inverter_model == 'PI18':
        protocol = 'PI18'
    else:
        protocol = None


    for name, data in commands.items():
        log.debug("Loading command information from {}".format(name))
        # Does this config data support the supplied inverter model?
        if isInverterSupported(inverter_model, data):
            log.info("... command {} loaded for inverter model: {}".format(getDataValue(data, 'name'), inverter_model))
            mpp_command = mppCommand(
                    getDataValue(data, 'name'),
                    getDataValue(data, 'description'),
                    getDataValue(data, 'type'),
                    getDataValue(data, 'response'),
                    getDataValue(data, 'test_responses'),
                    getDataValue(data, 'regex'),
                    help=getDataValue(data, 'help'),
                    crc_function=getDataValue(data, 'crc'),
                    prefix=getDataValue(data, 'prefix'),
                    protocol=protocol
            )
            COMMANDS.append(mpp_command)
    return COMMANDS

SERIAL_TYPE_TEST = 'serial_type_test'
SERIAL_TYPE_USB = 'serial_type_usb'
SERIAL_TYPE_ESP32 = 'serial_type_ESP32'
SERIAL_TYPE_SERIAL = 'serial_type_serial'


def isTestDevice(serial_device):
    """
    Determine if this instance is just a Test connection
    """
    if serial_device == 'TEST':
        return True
    return False


def isDirectUsbDevice(serial_device):
    """
    Determine if this instance is using direct USB connection
    (instead of a serial connection)
    """
    if not serial_device:
        return False
    match = re.search("^.*hidraw\\d$", serial_device)
    if match:
        log.debug("Device matches hidraw regex")
        return True
    match = re.search("^.*mppsolar\\d$", serial_device)
    if match:
        log.debug("Device matches mppsolar regex")
        return True
    return False

def isESP32Device(serial_device):
    return 'esp' in serial_device.lower()

def get_serial_type(serial_device):
    result = None
    if isTestDevice(serial_device):
        result = SERIAL_TYPE_TEST
    elif isDirectUsbDevice(serial_device):
        result = SERIAL_TYPE_USB
    elif isESP32Device(serial_device):
        result = SERIAL_TYPE_ESP32
    else:
        result = SERIAL_TYPE_SERIAL
    return result


class mppInverter:
    """
    MPP Solar Inverter Command Library
    - represents an inverter (and the commands the inverter supports)
    """

    def __init__(self, serial_device=None, baud_rate=2400, inverter_model='standard'):
        if not serial_device:
            raise NoDeviceError("A device to communicate by must be supplied, e.g. /dev/ttyUSB0")
        self._baud_rate = baud_rate
        self._serial_device = serial_device
        self._inverter_model = inverter_model
        self._serial_number = None
        self._serial_type = get_serial_type(serial_device)
        self._commands = getCommands(inverter_model)

    def __str__(self):
        """
        """
        inverter = "\n"
        inverter = SERIAL_TYPE_MESSAGE[self._serial_type].format(self._serial_device)
        inverter += "\n-------- List of supported commands --------\n"
        if self._commands:
            for cmd in self._commands:
                inverter += str(cmd)
        return inverter

    def getSerialNumber(self):
        if self._serial_number is None:
            result = self.execute("QID")
            # print (result)
            if result:
                response = result.getResponseDict()
                # print (byte_response)
                if response:
                    self._serial_number = response["serial_number"][0]
        return self._serial_number

    def getAllCommands(self):
        """
        Return list of defined commands
        """
        return self._commands

    def getResponse(self, cmd):
        """
        Execute command and return the byte_response
        """
        result = self.execute(cmd)
        if not result:
            return ""
        else:
            return result.getResponse()

    def getInfluxLineProtocol2(self, cmd):
        """
        Execute command and return the reponse as a Influx Line Protocol messages
        """
        result = self.execute(cmd)
        if not result:
            return ""
        else:
            return result.getInfluxLineProtocol2()

    def getInfluxLineProtocol(self, cmd):
        """
        Execute command and return the reponse as a Influx Line Protocol messages
        """
        result = self.execute(cmd)
        if not result:
            return ""
        else:
            return result.getInfluxLineProtocol()

    def getResponseDict(self, cmd):
        """
        Execute command and return the reponse as a dict
        """
        result = self.execute(cmd)
        if not result:
            return ""
        else:
            return result.getResponseDict()

    def _getCommand(self, cmd):
        """
        Returns the mppcommand object of the supplied cmd string
        """
        log.debug("Searching for cmd '{}'".format(cmd))
        if not self._commands:
            log.debug("No commands found")
            return None
        for command in self._commands:
            if not command.regex:
                if cmd == command.name:
                    return command
            else:
                match = command.regex.match(cmd)
                if match:
                    # log.debug(command.name, command.regex)
                    log.debug("Matched: {} Value: {}".format(command.name, match.group(1)))
                    command.setValue(match.group(1))
                    return command
        return None

    def _doTestCommand(self, command):
        """
        Performs a test command execution
        """
        log.info('TEST connection: executing %s', command)
        command.clearByteResponse()
        log.debug('Performing test command with %s', command)
        command.setByteResponse(command.getTestByteResponse())
        return command

    def _doSerialCommand(self, command):
        """
        Opens serial connection, sends command (multiple times if needed)
        and returns the byte_response
        """
        log.info('SERIAL connection: executing %s', command)
        command.clearByteResponse()
        response_line = None
        log.debug('port %s, baudrate %s', self._serial_device, self._baud_rate)
        try:
            with serial.serial_for_url(self._serial_device, self._baud_rate) as s:
                # Execute command multiple times, increase timeouts each time
                for x in range(1, 5):
                    log.debug('Command execution attempt %d...', x)
                    s.timeout = 1 + x
                    s.write_timeout = 1 + x
                    s.flushInput()
                    s.flushOutput()
                    s.write(command.byte_command)
                    time.sleep(0.5 * x)  # give serial port time to receive the data
                    response_line = s.readline()
                    log.debug('serial byte_response was: %s', response_line)
                    command.setByteResponse(response_line)
                    return command
        except Exception as e:
            log.warning("Serial read error: {}".format(e))
        log.info('Command execution failed')
        return command

    def _doESP32Command(self, command):
        """
        Uses ESP32 ESP32 for  serial connection, sends command (multiple times if needed)
        and returns the byte_response
        """
        log.info('ESP32 SERIAL connection: executing %s', command)
        command.clearByteResponse()
        uart_no = self._serial_device.lower().split('esp')[1]
        response_line = None
        log.debug('ESP32 UART #%s, baudrate %s', uart_no, self._baud_rate)
        uart = UART(uart_no, self._baud_rate)

        try:
            uart.init(self._baud_rate, timeout=1000)
            uart.write(command.byte_command)
            time.sleep(0.5 )  # give serial port time to receive the data
            response_line = uart.readline()
            log.debug('serial byte_response was: %s', response_line)
            command.setByteResponse(response_line)
        except Exception as e:
            log.warning("Serial read error: {}".format(e))
        log.info('Command execution failed')
        return command

    def _doDirectUsbCommand(self, command):
        """
        Opens direct USB connection, sends command (multiple times if needed)
        and returns the byte_response
        """
        log.info('DIRECT USB connection: executing %s', command)
        command.clearByteResponse()
        response_line = bytes()
        usb0 = None
        try:
            usb0 = os.open(self._serial_device, os.O_RDWR | os.O_NONBLOCK)
        except Exception as e:
            log.debug("USB open error: {}".format(e))
            return command
        # Send the command to the open usb connection
        to_send = command.byte_command
        try:
            log.debug("length of to_send: {}".format(len(to_send)))
        except:  # noqa: E722
            import pdb
            pdb.set_trace()
        if len(to_send) <= 8:
            # Send all at once
            log.debug("1 chunk send")
            time.sleep(0.35)
            os.write(usb0, to_send)
        elif len(to_send) > 8 and len(to_send) < 11:
            log.debug("2 chunk send")
            time.sleep(0.35)
            os.write(usb0, to_send[:5])
            time.sleep(0.35)
            os.write(usb0, to_send[5:])
        else:
            while (len(to_send) > 0):
                log.debug("multiple chunk send")
                # Split the byte command into smaller chucks
                send, to_send = to_send[:8], to_send[8:]
                log.debug("send: {}, to_send: {}".format(send, to_send))
                time.sleep(0.35)
                os.write(usb0, send)
        time.sleep(0.25)
        # Read from the usb connection
        # try to a max of 100 times
        for x in range(100):
            # attempt to deal with resource busy and other failures to read
            try:
                time.sleep(0.15)
                r = os.read(usb0, 256)
                response_line += r
            except Exception as e:
                log.debug("USB read error: {}".format(e))
            # Finished is \r is in byte_response
            if (bytes([13]) in response_line):
                # remove anything after the \r
                response_line = response_line[:response_line.find(bytes([13])) + 1]
                break
        log.debug('usb byte_response was: %s', response_line)
        command.setByteResponse(response_line)
        return command

    def execute(self, cmd):
        """
        Sends a command (as supplied) to inverter and returns the raw byte_response
        """
        command = self._getCommand(cmd)
        if command is None:
            log.critical("Command not found")
            return None
        return SERIAL_TYPE_DRIVER[self._serial_type](self, command)


SERIAL_TYPE_DRIVER = {
    SERIAL_TYPE_TEST : mppInverter._doTestCommand,
    SERIAL_TYPE_USB : mppInverter._doDirectUsbCommand,
    SERIAL_TYPE_ESP32 : mppInverter._doESP32Command,
    SERIAL_TYPE_SERIAL : mppInverter._doSerialCommand,
}

SERIAL_TYPE_MESSAGE = {
    SERIAL_TYPE_TEST : "Inverter connected as a {}",
    SERIAL_TYPE_USB : "Inverter connected via USB on {}",
    SERIAL_TYPE_ESP32 : "Inverter connected via UART on {}",
    SERIAL_TYPE_SERIAL : "Inverter connected via serial port on {}",
}

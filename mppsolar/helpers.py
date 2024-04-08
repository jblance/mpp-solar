#!/usr/bin/env python3
import logging
import importlib

log = logging.getLogger("helpers")


def get_kwargs(kwargs, key, default=None):
    return kwargs.get(key) or default


def key_wanted(key, filter=None, excl_filter=None):
    # remove any specifically excluded keys
    if excl_filter is not None and excl_filter.search(key):
        # log.debug(f"key_wanted: key {key} matches excl_filter {excl_filter} so key excluded")
        return False
    if filter is None:
        # log.debug(
        #    f"key_wanted: No filter and key {key} not excluded by excl_filter {excl_filter} so key wanted"
        # )
        return True
    elif filter.search(key):
        # log.debug(
        #    f"key_wanted: key {key} matches filter {filter} and not excl_filter {excl_filter} so key wanted"
        # )
        return True
    else:
        # log.debug(f"key_wanted: key {key} does not match filter {filter} so key excluded")
        return False


def get_value(_list, _index):
    """
    get the value from _list or return None if _index is out of bounds
    """
    # print(_list, len(_list))
    if _index >= len(_list):
        return None
    return _list[_index]


def get_resp_defn(key, defns):
    """
    look for a definition for the supplied key
    """
    # print(key, defns)
    if not key:
        return None
    if type(key) is bytes:
        try:
            key = key.decode("utf-8")
        except UnicodeDecodeError:
            log.info(f"key decode error for {key}")
    for defn in defns:
        if key == defn[0]:
            # print(key, defn)
            return defn
    # did not find definition for this key
    log.info(f"No defn found for {key} key")
    return [key, key, "", ""]


def get_device_class(device_type=None):
    """
    Take a device type string
    attempt to find and instantiate the corresponding module
    return class if found, otherwise return None
    """
    if device_type is None:
        return None
    device_type = device_type.lower()
    try:
        device_module = importlib.import_module("mppsolar.devices." + device_type, ".")
    except ModuleNotFoundError as e:
        # perhaps raise a mppsolar exception here??
        log.critical(f"Error loading device {device_type}: {e}")
        return None
    device_class = getattr(device_module, device_type)
    return device_class


def getMaxLen(data, index=0):
    _maxLen = 0
    for item in data:
        if type(item) == list:
            item = item[index]
        if type(item) == float or type(item) == int:
            item = str(item)
        if len(item) > _maxLen:
            _maxLen = len(item)
    return _maxLen

def get_max_response_length(data, index=0):
    return getMaxLen(data, index)

def pad(text, length):
    if type(text) == float or type(text) == int:
        text = str(text)
    if len(text) > length:
        return text
    return text.ljust(length, " ")

class CRC_XModem:
    def __init__(self, poly=0x1021, initial=0x0000):
        self.poly = poly
        self.initial = initial
        self.table = self.generate_crc_table()

    def generate_crc_table(self):
        table = [0] * 256
        for i in range(256):
            crc = i << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ self.poly
                else:
                    crc = crc << 1
            table[i] = crc & 0xFFFF
        return table

    def compute_crc(self, data):
        crc = self.initial
        for byte in data:
            crc = ((crc << 8) & 0xFFFF) ^ self.table[(crc >> 8) ^ byte]
        return crc

    def crc_hex(self, data):
        crc = self.compute_crc(data)
        return format(crc, '04x').upper()

""" formats / abstractformat.py """
import logging
import re
from abc import ABC, abstractmethod

from powermon.commands.reading import Reading
from powermon.commands.result import Result
# from powermon.device import DeviceInfo
from powermon.dto.formatDTO import FormatDTO

log = logging.getLogger("Formatter")


def pad(text, length):
    """ expand supplied value to 'length' with spaces, return unchanged if already longer """
    if isinstance(text, float) or isinstance(text, int):
        text = str(text)
    if len(text) > length:
        return text
    return text.ljust(length, " ")


def get_max_response_lengths(readings: list[Reading]):
    """ find the max length from a list of Readings """
    _max_name = 0
    _max_value = 0
    _max_unit = 0
    for reading in readings:
        _max_name = max(len(reading.data_name), _max_name)
        _max_value = max(len(str(reading.data_value)), _max_value)
        _max_unit = max(len(reading.data_unit), _max_unit)
    return _max_name, _max_value, _max_unit


class AbstractFormat(ABC):
    """ base for all format types """
    def __str__(self):
        return f"Format: {self.name}"

    def __init__(self, config=None):
        self.name = "AbstractFormat"
        if config is None:
            config = {}
        self.remove_spaces = config.get("remove_spaces", True)
        self.keep_case = config.get("keep_case", False)
        self.key_filter = config.get("filter", None)
        self.key_exclusion_filter = config.get("excl_filter", None)
        self.extra_info = config.get("extra_info", False)

    @property
    def key_filter(self):
        """ regular expression use to find keys wanted - or None to keep all """
        return getattr(self, "_key_filter", None)

    @key_filter.setter
    def key_filter(self, filter_string):
        if filter_string is not None:
            self._key_filter = re.compile(filter_string)

    @property
    def key_exclusion_filter(self):
        """ regular expression use to find keys to be excluded - or None to exclude none """
        return getattr(self, "_key_exclusion_filter", None)

    @key_exclusion_filter.setter
    def key_exclusion_filter(self, filter_string):
        if filter_string is not None:
            self._key_exclusion_filter = re.compile(filter_string)

    @abstractmethod
    def format(self, command, result: Result, device_info) -> list:
        """ entry point for all formats """

    def to_dto(self) -> FormatDTO:
        return FormatDTO(type=self.name)

    def format_and_filter_data(self, result: Result) -> list[Reading]:
        """ reformat key and remove unwanted readings """
        display_data = []
        for reading in result.readings:
            if reading is None:
                raise ValueError("reading cannot be None")
            formatted_key = self.format_key(reading.data_name)
            if self.is_key_wanted(formatted_key):
                display_data.append(reading)
        return display_data

    def format_key(self, key) -> str:
        """ reformat key """
        if self.remove_spaces:
            key = key.replace(" ", "_")
        if not self.keep_case:
            key = key.lower()
        return key

    def is_key_wanted(self, key) -> bool:
        """ determine if this item is wanted """
        # remove any specifically excluded keys
        if self.key_exclusion_filter is not None and self.key_exclusion_filter.search(key):
            # log.debug(f"key_wanted: key {key} matches excl_filter {excl_filter} so key excluded")
            return False
        if self.key_filter is None:
            # log.debug(
            #    f"key_wanted: No filter and key {key} not excluded by excl_filter {excl_filter} so key wanted"
            # )
            return True
        elif self.key_filter.search(key):
            # log.debug(
            #    f"key_wanted: key {key} matches filter {filter} and not excl_filter {excl_filter} so key wanted"
            # )
            return True
        else:
            # log.debug(f"key_wanted: key {key} does not match filter {filter} so key excluded")
            return False

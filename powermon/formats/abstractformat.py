from abc import ABC, abstractmethod
import logging
import re


# from time import sleep
log = logging.getLogger("Formatter")


class AbstractFormat(ABC):
    def __str__(self):
        return f"Format: {self.name}"

    def __init__(self, formatConfig):
        self.name = "AbstractFormat"
        self.remove_spaces = formatConfig.get("remove_spaces", True)
        self.keep_case = formatConfig.get("keep_case", False)

        self._keyFilter = None
        _keyFilterString = formatConfig.get("filter", None)
        if _keyFilterString is not None:
            self._keyFilter = re.compile(_keyFilterString)

        self._keyExclusionfilter = None
        _keyExclusionFilterString = formatConfig.get("excl_filter", None)
        if _keyExclusionFilterString is not None:
            self._keyExclusionfilter = re.compile(_keyExclusionFilterString)

    @abstractmethod
    def format(self, data):
        pass

    # Override this if the format sends multiple messages
    def sendsMultipleMessages(self) -> bool:
        return False

    def formatAndFilterData(self, data):
        # TODO: should we make data a proper object so it's easy to get the data we want?
        # remove raw response
        if "raw_response" in data:
            data.pop("raw_response")
        # remove command details
        if "_command" in data:
            data.pop("_command")
        if "_command_description" in data:
            data.pop("_command_description")

        displayData = {}
        for key in data:
            _values = data[key]
            formattedKey = self.formatKey(key)
            if self.isKeyWanted(formattedKey):
                displayData[formattedKey] = _values
        return displayData

    def formatKey(self, key) -> str:
        if self.remove_spaces:
            key = key.replace(" ", "_")
        if not self.keep_case:
            key = key.lower()
        return key

    def isKeyWanted(self, key) -> bool:
        # remove any specifically excluded keys
        if self._keyExclusionfilter is not None and self._keyExclusionfilter.search(key):
            # log.debug(f"key_wanted: key {key} matches excl_filter {excl_filter} so key excluded")
            return False
        if self._keyFilter is None:
            # log.debug(
            #    f"key_wanted: No filter and key {key} not excluded by excl_filter {excl_filter} so key wanted"
            # )
            return True
        elif self._keyFilter.search(key):
            # log.debug(
            #    f"key_wanted: key {key} matches filter {filter} and not excl_filter {excl_filter} so key wanted"
            # )
            return True
        else:
            # log.debug(f"key_wanted: key {key} does not match filter {filter} so key excluded")
            return False

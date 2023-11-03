from abc import ABC, abstractmethod
import logging
import re

from powermon.dto.formatDTO import FormatDTO
from powermon.commands.result import Result
from powermon.commands.reading import Reading


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
    def set_command_description(self, command_description):
        pass

    @abstractmethod
    def format(self, result: Result) -> list:
        pass

    def to_dto(self) -> FormatDTO:
        return FormatDTO(type=self.name)
    
    # Override this if the format sends multiple messages
    def sendsMultipleMessages(self) -> bool:
        return False

    def format_and_filter_data(self, result: Result) -> list[Reading]:

        display_data = []
        for response in result.get_responses():
            if response is None:
                raise ValueError("response cannot be None")
            formatted_key = self.formatKey(response.get_data_name())
            if self.isKeyWanted(formatted_key):
                display_data.append(response)
        return display_data

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

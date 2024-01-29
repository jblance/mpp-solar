""" reading.py """
from powermon.dto.reading_dto import ReadingDTO


class Reading:
    """ class to contain the raw reading, processed reading and reading definition for a particular reading """
    def __str__(self):
        return f"Reading: {self.data_name=}, {self.data_value=}, {self.data_unit=}, {self.is_valid=}"

    def __init__(self, data_name: str, data_value: str, data_unit: str, device_class: str = None, state_class: str = None, icon: str = None) -> None:
        self.data_name = data_name
        self.data_value = data_value
        self.data_unit = data_unit
        self.device_class = device_class
        self.icon = icon
        self.state_class = state_class
        self.is_valid = True

    def to_dto(self) -> ReadingDTO:
        """ convert Reading to a data transfer object """
        return ReadingDTO(data_name=self.get_data_name(), data_value=self.get_data_value(), data_unit=self.get_data_unit())

    @property
    def raw_value(self):
        """ the raw reading returned from the device - as returned """
        return self._raw_value

    @raw_value.setter
    def raw_value(self, value):
        self._raw_value = value

    @property
    def processed_value(self):
        """ the reading after processing and conversion - the reading we want to see """
        return self._processed_value

    @processed_value.setter
    def processed_value(self, value):
        # should take raw value and 'process it'
        self._processed_value = value

    @property
    def reading_definition(self):
        """ the reading definition associated with this reading """
        return self._reading_definition

    @reading_definition.setter
    def reading_definition(self, value):
        self._reading_definition = value

    # the below are / should be part of reading definition
    def get_data_name(self) -> str:
        return self.data_name.replace(" ", "_").lower()

    def get_data_unit(self) -> str:
        if self.data_unit is None:
            return ""
        return self.data_unit

    def get_data_value(self) -> str:
        return self.data_value

    def get_icon(self) -> str | None:
        return self.icon

    def get_device_class(self) -> str | None:
        return self.device_class

    def get_state_class(self) -> str | None:
        return self.state_class

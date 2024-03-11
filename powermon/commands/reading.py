""" reading.py """
from powermon.dto.reading_dto import ReadingDTO


class Reading:
    """ class to contain the raw reading, processed reading and reading definition for a particular reading """
    def __str__(self):
        return f"Reading: {self.data_name=}, {self.data_value=}, {self.data_unit=}, {self.is_valid=}"

    # def __init__(self, data_name: str, data_value: str, data_unit: str, device_class: str = None, state_class: str = None, icon: str = None) -> None:
    def __init__(self, raw_value, processed_value, definition) -> None:
        self.raw_value = raw_value
        self.processed_value = processed_value
        self.definition = definition
        self.is_valid = True

    def to_dto(self) -> ReadingDTO:
        """ convert Reading to a data transfer object """
        return ReadingDTO(data_name=self.data_name, data_value=self.data_value, data_unit=self.data_unit)

    @property
    def raw_value(self):
        """ the raw reading returned from the device - as returned """
        return getattr(self, "_raw_value", None)

    @raw_value.setter
    def raw_value(self, value):
        self._raw_value = value

    @property
    def processed_value(self):
        """ the reading after processing and conversion - the reading we want to see """
        return getattr(self, "_processed_value", None)

    @processed_value.setter
    def processed_value(self, value):
        # should take raw value and 'process it'
        self._processed_value = value

    @property
    def definition(self):
        """ the reading definition associated with this reading """
        return getattr(self, "_definition", None)

    @definition.setter
    def definition(self, value):
        self._definition = value

    # the below are / should be part of reading definition
    @property
    def data_name(self) -> str:
        return self.definition.description

    @property
    def data_unit(self) -> str:
        if self.definition.unit is None:
            return ""
        return self.definition.unit

    @property
    def data_value(self) -> str:
        return self.processed_value

    @property
    def icon(self) -> str | None:
        return self.definition.icon

    @property
    def device_class(self) -> str | None:
        return self.definition.device_class

    @property
    def state_class(self) -> str | None:
        return self.definition.state_class

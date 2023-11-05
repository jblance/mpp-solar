""" reading.py """
# from enum import auto
# from strenum import LowercaseStrEnum

from powermon.dto.reading_dto import ReadingDTO


class Reading:
    def __str__(self):
        return f"Reading: {self.data_name=}, {self.data_value=}, {self.data_unit=}, {self.is_valid=}"

    def __init__(self, data_name: str,
                 data_value: str,
                 data_unit: str,
                 device_class: str = None,
                 state_class: str = None,
                 icon: str = None) -> None:
        self.data_name = data_name
        self.data_value = data_value
        self.data_unit = data_unit
        self.device_class = device_class
        self.icon = icon
        self.state_class = state_class
        self.is_valid = True

    def to_dto(self) -> ReadingDTO:
        return ReadingDTO(data_name=self.get_data_name(), data_value=self.get_data_value(), data_unit=self.get_data_unit())

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

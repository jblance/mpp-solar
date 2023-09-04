"""
config_model.py - pydantic definitions for the powermon config model
"""

from typing import Literal, List
from pydantic import BaseModel, Extra  # pylint: disable=E0401


class NoExtraBaseModel(BaseModel):
    """ updated BaseModel with Extras forbidden """
    class Config:
        """pydantic BaseModel config"""
        extra = Extra.forbid

class DaemonConfig(NoExtraBaseModel):
    """ model/allowed elements for daemon section of config """
    type: None | str
    keepalive: None | str


class MQTTConfig(NoExtraBaseModel):
    """ model/allowed elements for mqtt broker section of config """
    name: str
    port: None | int
    username: None | str
    password: None | str


class APIConfig(NoExtraBaseModel):
    """ model/allowed elements for api section of config """
    host: None | str
    port: None | int
    enabled: None | bool
    log_level: None | str
    announce_topic: None | str
    adhoc_topic: None | str
    refresh_interval: None | int


class BaseFormatConfig(NoExtraBaseModel):
    """ model/allowed elements for base format config """
    type: str
    tag: None | str
    draw_lines: None | bool
    keep_case: None | bool
    remove_spaces: None | bool
    extra_info: None | bool
    excl_filter: None | str
    filter: None | str


class HassFormatConfig(BaseFormatConfig):
    """ model/allowed elements for hass format config """
    discovery_prefix: None | str
    entity_id_prefix: None | str


class MqttFormatConfig(BaseFormatConfig):
    """ model/allowed elements for mqtt format config """
    topic: None | str


class LoopsTriggerConfig(NoExtraBaseModel):
    """ model/allowed elements for 'loops' trigger config """
    loops: int


class AtTriggerConfig(NoExtraBaseModel):
    """ model/allowed elements for 'at' trigger config """
    at: str


class EveryTriggerConfig(NoExtraBaseModel):
    """ model/allowed elements for 'every' trigger config """
    every: int


class OutputConfig(NoExtraBaseModel):
    """ model/allowed elements for output config """
    type: Literal['screen'] | Literal['mqtt'] | Literal['api_mqtt']
    format: None | str | BaseFormatConfig | HassFormatConfig | MqttFormatConfig


class CommandConfig(NoExtraBaseModel):
    """ model/allowed elements for command section of config """
    command: str
    type: None | Literal["basic"] | Literal["poll"]
    trigger: None | LoopsTriggerConfig | AtTriggerConfig | EveryTriggerConfig
    outputs: None | str | List[OutputConfig]


class SerialPortConfig(BaseModel):
    """ model/allowed elements for serial port config """
    type: Literal["serial"]
    path: str
    baud: None | int
    protocol: None | str


class UsbPortConfig(BaseModel):
    """ model/allowed elements for usb port config """
    type: Literal["usb"]
    path: None | str
    protocol: None | str


class TestPortConfig(BaseModel):
    """ model/allowed elements for test port config """
    type: Literal["test"]
    response_number: None | int
    protocol: None | str


class DeviceConfig(NoExtraBaseModel):
    """ model/allowed elements for device section of config """
    name: None | str
    id: None | str
    model: None | str
    manufacturer: None | str
    port: SerialPortConfig | UsbPortConfig | TestPortConfig


class BaseConfig(NoExtraBaseModel):
    """ model/allowed elements for first level of config """
    device: DeviceConfig
    commands: List[CommandConfig]
    mqttbroker: None | MQTTConfig
    api: None | APIConfig
    daemon: None | DaemonConfig
    debuglevel: None | str
    loop: None | int | Literal["once"]


class ConfigModel(NoExtraBaseModel):
    """Entry point for config model"""
    config: BaseConfig

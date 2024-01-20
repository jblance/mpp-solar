"""
config_model.py - pydantic definitions for the powermon config model
"""

from typing import Literal, List
from pydantic import BaseModel, Extra, Field


class NoExtraBaseModel(BaseModel):
    """ updated BaseModel with Extras forbidden """
    class Config:
        """pydantic BaseModel config"""
        extra = Extra.forbid


class DaemonConfig(NoExtraBaseModel):
    """ model/allowed elements for daemon section of config """
    type: None | str
    keepalive: None | int


class MQTTConfig(NoExtraBaseModel):
    """ model/allowed elements for mqtt broker section of config """
    name: str
    port: None | int = Field(default=None)
    username: None | str = Field(default=None)
    password: None | str = Field(default=None)


class APIConfig(NoExtraBaseModel):
    """ model/allowed elements for api section of config """
    host: None | str = Field(default=None)
    port: None | int = Field(default=None)
    enabled: None | bool = Field(default=False)
    log_level: None | str = Field(default=None)
    announce_topic: None | str = Field(default=None)
    adhoc_topic: None | str = Field(default=None)
    refresh_interval: None | int = Field(default=None)


class BaseFormatConfig(NoExtraBaseModel):
    """ model/allowed elements for base format config """
    type: str
    tag: None | str = Field(default=None)
    draw_lines: None | bool = Field(default=None)
    keep_case: None | bool = Field(default=None)
    remove_spaces: None | bool = Field(default=None)
    extra_info: None | bool = Field(default=None)
    excl_filter: None | str = Field(default=None)
    filter: None | str = Field(default=None)


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
    type: Literal['screen'] | Literal['mqtt'] | Literal['api_mqtt'] | Literal['table']
    format: None | str | BaseFormatConfig | HassFormatConfig | MqttFormatConfig = Field(default=None)


class CommandConfig(NoExtraBaseModel):
    """ model/allowed elements for command section of config """
    command: str
    type: None | Literal["basic"] | Literal["poll"] = Field(default="basic")
    override: None | dict = Field(default=None)
    trigger: None | LoopsTriggerConfig | AtTriggerConfig | EveryTriggerConfig = Field(default=None)
    outputs: None | List[OutputConfig] | str = Field(default=None)


class SerialPortConfig(BaseModel):
    """ model/allowed elements for serial port config """
    type: Literal["serial"]
    path: str
    baud: None | int  = Field(default=None)
    protocol: None | str


class UsbPortConfig(BaseModel):
    """ model/allowed elements for usb port config """
    type: Literal["usb"]
    path: None | str
    protocol: None | str


class TestPortConfig(BaseModel):
    """ model/allowed elements for test port config """
    type: Literal["test"]
    response_number: None | int = Field(default=None)
    protocol: None | str = Field(default=None)


class DeviceConfig(NoExtraBaseModel):
    """ model/allowed elements for device section of config """
    name: None | str = Field(default=None)
    id: None | str | int = Field(default=None)
    model: None | str = Field(default=None)
    manufacturer: None | str = Field(default=None)
    port: TestPortConfig | SerialPortConfig | UsbPortConfig


class BaseConfig(NoExtraBaseModel):
    """ model/allowed elements for first level of config """
    device: DeviceConfig
    commands: List[CommandConfig]
    mqttbroker: None | MQTTConfig = Field(default=None)
    api: None | APIConfig = Field(default=None)
    daemon: None | DaemonConfig = Field(default=None)
    debuglevel: None | int | str = Field(default=None)  # If you put "debug" it translates to 10 then fails to load the config
    loop: None | int | Literal["once"] = Field(default=None)


class ConfigModel(NoExtraBaseModel):
    """Entry point for config model"""
    config: BaseConfig

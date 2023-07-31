from typing import Literal, List

from pydantic import BaseModel, Extra


class DaemonConfig(BaseModel):
    type: None | str
    keepalive: None | str

    class Config:
        extra = Extra.forbid


class MQTTConfig(BaseModel):
    name: str
    port: None | int
    username: None | str
    password: None | str

    class Config:
        extra = Extra.forbid


class APIConfig(BaseModel):
    host: None | str
    port: None | int
    enabled: None | bool
    log_level: None | str
    announce_topic: None | str
    adhoc_topic: None | str
    refresh_interval: None | int

    class Config:
        extra = Extra.forbid


class BaseFormatConfig(BaseModel):
    type: str
    tag: None | str
    draw_lines: None | bool
    keep_case: None | bool
    remove_spaces: None | bool
    extra_info: None | bool
    excl_filter: None | str
    filter: None | str

    class Config:
        extra = Extra.forbid


class HassFormatConfig(BaseFormatConfig):
    discovery_prefix: None | str
    entity_id_prefix: None | str

    class Config:
        extra = Extra.forbid


class MqttFormatConfig(BaseFormatConfig):
    topic: None | str

    class Config:
        extra = Extra.forbid


class LoopsTriggerConfig(BaseModel):
    loops: int

    class Config:
        extra = Extra.forbid


class AtTriggerConfig(BaseModel):
    at: str

    class Config:
        extra = Extra.forbid


class EveryTriggerConfig(BaseModel):
    every: int

    class Config:
        extra = Extra.forbid


class OutputConfig(BaseModel):
    type: Literal['screen'] | Literal['mqtt']
    format: None | str | BaseFormatConfig | HassFormatConfig | MqttFormatConfig

    class Config:
        extra = Extra.forbid


class CommandConfig(BaseModel):
    command: str
    type: None | Literal["basic"] | Literal["poll"]
    trigger: None | LoopsTriggerConfig | AtTriggerConfig | EveryTriggerConfig
    outputs: None | str | List[OutputConfig]

    class Config:
        extra = Extra.forbid


class SerialPortConfig(BaseModel):
    type: Literal["serial"]
    path: str
    baud: None | int
    protocol: None | str


class UsbPortConfig(BaseModel):
    type: Literal["usb"]
    path: None | str
    protocol: None | str


class TestPortConfig(BaseModel):
    type: Literal["test"]
    response_number: None | int
    protocol: None | str


class DeviceConfig(BaseModel):
    name: None | str
    id: None | str
    model: None | str
    manufacturer: None | str
    port: SerialPortConfig | UsbPortConfig | TestPortConfig

    class Config:
        extra = Extra.forbid


class BaseConfig(BaseModel):
    device: DeviceConfig
    commands: List[CommandConfig]
    mqttbroker: None | MQTTConfig
    api: None | APIConfig
    daemon: None | DaemonConfig
    debuglevel: None | str
    loop: None | int | Literal["once"]

    class Config:
        extra = Extra.forbid


class ConfigModel(BaseModel):
    config: BaseConfig

    class Config:
        extra = Extra.forbid

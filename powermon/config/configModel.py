from typing import Optional

from pydantic import BaseModel, Extra


class DaemonConfig(BaseModel):
    type: Optional[str]
    keepalive: Optional[str]

    class Config:
        extra = Extra.forbid


class MQTTConfig(BaseModel):
    name: str
    port = 1883
    username: Optional[str]
    password: Optional[str]

    class Config:
        extra = Extra.forbid


class APIConfig(BaseModel):
    announce_topic: Optional[str]
    adhoc_topic: Optional[str]
    enabled: Optional[bool]

    class Config:
        extra = Extra.forbid


class CommandConfig(BaseModel):
    command: str
    type = "basic"
    trigger: Optional[dict]
    outputs: Optional[str | list | dict]

    class Config:
        extra = Extra.forbid


class PortConfig(BaseModel):
    type: str
    path: Optional[str]
    baud: Optional[int]
    response_number: Optional[int]
    protocol: str

    class Config:
        extra = Extra.forbid


class DeviceConfig(BaseModel):
    name = "unnamed_device"
    id: Optional[str]
    model: Optional[str]
    manufacturer: Optional[str]
    port: PortConfig

    class Config:
        extra = Extra.forbid


class BaseConfig(BaseModel):
    device: DeviceConfig
    commands: list[CommandConfig]
    mqttbroker: Optional[MQTTConfig]
    api: Optional[APIConfig]
    daemon: Optional[DaemonConfig]
    debuglevel: Optional[str]

    class Config:
        extra = Extra.forbid


class ConfigModel(BaseModel):
    config: BaseConfig

    class Config:
        extra = Extra.forbid

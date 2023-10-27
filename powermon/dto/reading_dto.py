from pydantic import BaseModel, Field


class ReadingDTO(BaseModel):
    data_name: str
    data_value: str
    data_unit: str = Field(default="")
    extra_info: dict = Field(default={})
    icon: str | None = Field(default=None)
    device_class: str | None = Field(default=None)
    state_class: str | None = Field(default=None)
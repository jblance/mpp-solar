from pydantic import BaseModel, Field


class ResponseDTO(BaseModel):
    data_name: str
    data_value: str
    data_unit: str = Field(default="")
    extra_info: dict = Field(default={})
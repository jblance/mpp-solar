class Response:
    def __init__(self, name: str, data_value: str, data_unit: str, extra_info: str = None) -> None:
        self.name = name
        self.data_value = data_value
        self.data_unit = data_unit
        self.extra_info = extra_info
        
    @classmethod
    def from_config(cls, response_config: dict) -> "Response":
        name = response_config.get("name")
        data_value = response_config.get("data_value")
        data_unit = response_config.get("data_unit")
        extra_info = response_config.get("extra_info")
        return cls(name=name, data_value=data_value, data_unit=data_unit, extra_info=extra_info)
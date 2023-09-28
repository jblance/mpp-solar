class Response:
    def __init__(self, data_name: str, data_value: str, data_unit: str, extra_info: str = None) -> None:
        self.data_name = data_name
        self.data_value = data_value
        self.data_unit = data_unit
        self.extra_info = extra_info
        self.is_valid = True
        
    def get_data_name(self) -> str:
        return self.data_name.replace(" ", "_").lower()
    
    def get_data_unit(self) -> str:
        return self.data_unit
    
    def get_data_value(self) -> str:
        return self.data_value
        
    @classmethod
    def from_config(cls, response_config: dict) -> "Response":
        name = response_config.get("name")
        data_value = response_config.get("data_value")
        data_unit = response_config.get("data_unit")
        extra_info = response_config.get("extra_info")
        return cls(data_name=name, data_value=data_value, data_unit=data_unit, extra_info=extra_info)
class Response:
    def __init__(self, data_name: str, data_value: str, data_unit: str, extra_info: dict = None) -> None:
        self.data_name = data_name
        self.data_value = data_value
        self.data_unit = data_unit
        self.extra_info = extra_info
        self.is_valid = True
        
    def get_data_name(self) -> str:
        return self.data_name.replace(" ", "_").lower()
    
    def get_data_unit(self) -> str:
        if self.data_unit is None:
            return ""
        return self.data_unit
    
    def get_data_value(self) -> str:
        return self.data_value
    
    def get_extra_info(self) -> dict:
        return self.extra_info
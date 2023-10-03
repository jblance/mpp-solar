from powermon.dto.response_dto import ResponseDTO

class Response:
    def __init__(self, data_name: str, data_value: str, data_unit: str, extra_info: dict = None) -> None:
        self.data_name = data_name
        self.data_value = data_value
        self.data_unit = data_unit
        self.extra_info = extra_info
        self.is_valid = True
        
    def to_DTO(self) -> ResponseDTO:
        return ResponseDTO(data_name=self.get_data_name(), data_value=self.get_data_value(), data_unit=self.get_data_unit(), extra_info=self.get_extra_info())
    
    def __str__(self):
        return f"Response: {self.data_name=}, {self.data_value=}, {self.data_unit=}, {self.extra_info=}"
        
    def get_data_name(self) -> str:
        return self.data_name.replace(" ", "_").lower()
    
    def get_data_unit(self) -> str:
        if self.data_unit is None:
            return ""
        return self.data_unit
    
    def get_data_value(self) -> str:
        return self.data_value
    
    def get_extra_info(self) -> dict:
        if self.extra_info is None:
            return {}
        return self.extra_info
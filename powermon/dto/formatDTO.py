""" dto / formatDTO.py """
from pydantic import BaseModel


class FormatDTO(BaseModel):
    """ data transfer object for format objects """
    type: str

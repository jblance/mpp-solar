from typing import Optional

from pydantic import BaseModel


class ApicoordinatorDTO(BaseModel):
    name: str
    description: Optional[str]

from typing import Optional
from pydantic import validator
from schemas import Model


class AutoTagRead(Model):
    name: Optional[str]
    nameKZ: Optional[str]
    
    @validator("nameKZ", "name", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else ""
    

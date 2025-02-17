from typing import Any, Optional
from pydantic import BaseModel, validator


class AutoTagRead(BaseModel):
    name: Optional[str]
    nameKZ: Optional[str]
    
    @validator("nameKZ", "name", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else ""
    

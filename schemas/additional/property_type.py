import uuid
from typing import Optional

from pydantic import BaseModel


class PropertyTypeBase(BaseModel):
    name: str
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PropertyTypeCreate(PropertyTypeBase):
    pass


class PropertyTypeUpdate(PropertyTypeBase):
    pass


class PropertyTypeRead(PropertyTypeBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

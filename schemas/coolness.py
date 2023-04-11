import uuid
from typing import Optional, Union

from pydantic import BaseModel
from datetime import datetime


class CoolnessTypeBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CoolnessTypeCreate(CoolnessTypeBase):
    pass


class CoolnessTypeUpdate(CoolnessTypeBase):
    pass


class CoolnessTypeRead(CoolnessTypeBase):
    id: uuid.UUID
    name: str


class CoolnessBase(BaseModel):
    type_id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    name: Optional[str]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CoolnessCreate(CoolnessBase):
    pass


class CoolnessUpdate(CoolnessBase):
    pass


class CoolnessRead(CoolnessBase):
    
    id: Optional[uuid.UUID]
    type: Optional[CoolnessTypeRead]

import uuid
from typing import Optional, Union

from pydantic import BaseModel
from datetime import datetime


class CoolnessBase(BaseModel):
    type_id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CoolnessCreate(CoolnessBase):
    pass


class CoolnessUpdate(CoolnessBase):
    pass


class CoolnessRead(CoolnessBase):

    id: Optional[uuid.UUID] 

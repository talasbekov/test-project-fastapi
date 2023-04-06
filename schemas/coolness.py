import uuid
from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class CoolnessBase(BaseModel):
    speciality: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
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

     

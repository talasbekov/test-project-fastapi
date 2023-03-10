import uuid
import datetime

from pydantic import BaseModel
from typing import Optional


class PropertiesBase(BaseModel):
    type_id: uuid.UUID
    purchase_date: datetime.datetime
    address: str
    profile_id: uuid.UUID
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PropertiesCreate(PropertiesBase):
    pass


class PropertiesUpdate(PropertiesBase):
    pass


class PropertiesRead(PropertiesBase):
    id: Optional[uuid.UUID]

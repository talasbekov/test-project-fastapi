import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel
from .property_type import PropertyTypeRead


class PropertiesBase(Model):
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


class PropertiesRead(PropertiesBase, ReadModel):
    type: Optional[PropertyTypeRead]

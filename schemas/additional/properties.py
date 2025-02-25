import datetime
import uuid
from typing import Optional


from schemas import Model, ReadModel
from .property_type import PropertyTypeRead


class PropertiesBase(Model):
    type_id: str
    purchase_date: datetime.datetime
    purchase_type: Optional[str] = None
    purchase_typeKZ: Optional[str] = None
    address: str
    profile_id: str
    document_link: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PropertiesCreate(PropertiesBase):
    pass


class PropertiesUpdate(PropertiesBase):
    pass


class PropertiesRead(PropertiesBase, ReadModel):
    type_id: Optional[str]
    type: Optional[PropertyTypeRead]

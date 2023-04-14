import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel
from .property_type import PropertyTypeRead


class ServiceHousingBase(Model):

    type_id: uuid.UUID
    address: str
    issue_date: datetime.datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ServiceHousingCreate(ServiceHousingBase):
    pass


class ServiceHousingUpdate(ServiceHousingBase):
    pass


class ServiceHousingRead(ServiceHousingBase, ReadModel):
    type_id: Optional[uuid.UUID]
    address: Optional[str]
    issue_date: Optional[datetime.datetime]

    type: Optional[PropertyTypeRead]

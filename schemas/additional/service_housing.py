import datetime
import uuid
from typing import Optional

from pydantic import AnyUrl

from schemas import Model, ReadModel
from .property_type import PropertyTypeRead


class ServiceHousingBase(Model):

    type_id: str
    address: str
    document_link: Optional[AnyUrl]
    issue_date: datetime.datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ServiceHousingCreate(ServiceHousingBase):
    pass


class ServiceHousingUpdate(ServiceHousingBase):
    pass


class ServiceHousingRead(ServiceHousingBase, ReadModel):
    type_id: Optional[str]
    address: Optional[str]
    issue_date: Optional[datetime.datetime]

    type: Optional[PropertyTypeRead]

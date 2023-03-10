import datetime
import uuid

from pydantic import BaseModel
from typing import Optional

from .property_type import PropertyTypeRead

class ServiceHousingBase(BaseModel):

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


class ServiceHousingRead(ServiceHousingBase):

    id: Optional[uuid.UUID]
    type_id: Optional[uuid.UUID]
    address: Optional[str]
    issue_date: Optional[datetime.datetime]

    type: Optional[PropertyTypeRead]

import datetime
import uuid
from typing import Optional

from pydantic import AnyUrl, BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class DispensaryRegistrationBase(NamedModel):
    initiator: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    document_link: AnyUrl
    profile_id: uuid.UUID


class DispensaryRegistrationCreate(DispensaryRegistrationBase):
    pass


class DispensaryRegistrationUpdate(DispensaryRegistrationBase):
    pass


class DispensaryRegistrationRead(DispensaryRegistrationBase, ReadNamedModel):
    document_link: Optional[str]
    initiator: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    profile_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True

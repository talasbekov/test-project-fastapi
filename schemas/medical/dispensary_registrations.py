import datetime
import uuid
from typing import Optional

from pydantic import BaseModel




class DispensaryRegistrationBase(BaseModel):
    name: str
    initiator: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    document_link: str
    profile_id: uuid.UUID


class DispensaryRegistrationCreate(DispensaryRegistrationBase):
    pass


class DispensaryRegistrationUpdate(DispensaryRegistrationBase):
    pass


class DispensaryRegistrationRead(DispensaryRegistrationBase):
    id: uuid.UUID

    document_link: Optional[str]
    name: Optional[str]
    initiator: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    profile_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True

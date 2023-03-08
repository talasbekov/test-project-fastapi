import datetime
import uuid
from typing import Optional

from pydantic import BaseModel




class DispensaryRegistrationBase(BaseModel):
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

    class Config:
        orm_mode = True

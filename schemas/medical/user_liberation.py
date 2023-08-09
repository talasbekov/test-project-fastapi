import datetime
import uuid
from typing import Optional

from pydantic import BaseModel


class UserLiberationBase(BaseModel):
    reason: str
    liberation_id: str
    initiator: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    profile_id: str
    document_link: Optional[str]


class UserLiberationCreate(UserLiberationBase):
    pass


class UserLiberationUpdate(UserLiberationBase):
    pass


class UserLiberationRead(UserLiberationBase):
    id: Optional[str]
    reason: Optional[str]
    liberation_id: Optional[str]
    initiator: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    profile_id: Optional[str]

    class Config:
        orm_mode = True

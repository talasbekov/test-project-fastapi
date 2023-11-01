import datetime
import uuid
from typing import Optional, List

from pydantic import BaseModel


class UserLiberationBase(BaseModel):
    reason: str
    liberation_ids: List
    initiator: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    profile_id: str
    document_link: Optional[str]


class UserLiberationCreate(UserLiberationBase):
    liberation_ids: Optional[List]


class UserLiberationUpdate(UserLiberationBase):
    liberation_ids: Optional[List]


class UserLiberationRead(UserLiberationBase):
    id: Optional[str]
    reason: Optional[str]
    liberation_ids: Optional[List]
    initiator: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    profile_id: Optional[str]

    class Config:
        orm_mode = True

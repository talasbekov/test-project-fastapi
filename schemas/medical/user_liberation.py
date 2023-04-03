import datetime
import uuid
from typing import Optional, List

from pydantic import BaseModel

from .liberation import LiberationRead


class UserLiberationBase(BaseModel):
    reason: str
    liberation_id: uuid.UUID
    initiator: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    profile_id: uuid.UUID


class UserLiberationCreate(UserLiberationBase):
    pass


class UserLiberationUpdate(UserLiberationBase):
    pass


class UserLiberationRead(UserLiberationBase):
    id: Optional[uuid.UUID]
    reason: Optional[str]
    liberation_id: Optional[uuid.UUID]
    initiator: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    profile_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True

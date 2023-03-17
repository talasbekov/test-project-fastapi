import datetime
import uuid
from typing import Optional

from pydantic import BaseModel


class UserLiberationsBase(BaseModel):
    reason: str
    liberation_name: str
    initiator: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    profile_id: uuid.UUID


class UserLiberationsCreate(UserLiberationsBase):
    pass


class UserLiberationsUpdate(UserLiberationsBase):
    pass


class UserLiberationsRead(UserLiberationsBase):
    id: Optional[uuid.UUID]
    reason: Optional[str]
    liberation_name: Optional[str]
    initiator: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    profile_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True

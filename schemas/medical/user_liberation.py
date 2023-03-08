import datetime
import uuid

from pydantic import BaseModel

class UserLiberationsBase(BaseModel):
    reason: str
    liberation_name: str
    initiator: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    profile_id: str


class UserLiberationsCreate(UserLiberationsBase):
    pass


class UserLiberationsUpdate(UserLiberationsBase):
    pass


class UserLiberationsRead(UserLiberationsBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

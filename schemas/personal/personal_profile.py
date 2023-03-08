import uuid
import datetime

from typing import Optional, List

from pydantic import BaseModel


# base
class PersonalProfileBase(BaseModel):
    profile_id: uuid.UUID


# create
class PersonalProfileCreate(PersonalProfileBase):
    pass


# update
class PersonalProfileUpdate(PersonalProfileBase):
    pass


# read
class PersonalProfileRead(PersonalProfileBase):
    id: Optional[uuid.UUID]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True

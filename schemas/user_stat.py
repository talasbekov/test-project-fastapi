import uuid

from pydantic import BaseModel
from typing import Optional


class UserStatBase(BaseModel):
    user_id: uuid.UUID
    physical_training: int
    fire_training: int
    attendance: int
    activity: int
    opinion_of_colleagues: int
    opinion_of_management: int


class UserStatCreate(UserStatBase):
    pass


class UserStatUpdate(UserStatBase):
    pass


class UserStatRead(UserStatBase):
    id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    physical_training: Optional[int]
    fire_training: Optional[int]
    attendance: Optional[int]
    activity: Optional[int]
    opinion_of_colleagues: Optional[int]
    opinion_of_management: Optional[int]

    class Config:
        orm_mode = True

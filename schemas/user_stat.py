import uuid
from typing import Optional

from schemas import Model, ReadModel


class UserStatBase(Model):
    user_id: str
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


class UserStatRead(UserStatBase, ReadModel):
    user_id: Optional[str]
    physical_training: Optional[int]
    fire_training: Optional[int]
    attendance: Optional[int]
    activity: Optional[int]
    opinion_of_colleagues: Optional[int]
    opinion_of_management: Optional[int]

    class Config:
        orm_mode = True

import uuid

from pydantic import BaseModel


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
    id: uuid.UUID

    class Config:
        orm_mode = True

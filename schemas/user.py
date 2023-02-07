import uuid
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    middle_name: str
    group_id: Optional[str]
    call_sign: str
    id_number: str
    phone_number: str
    address: str
    birthday: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

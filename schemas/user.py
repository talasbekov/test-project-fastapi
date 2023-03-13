import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from schemas import (BadgeRead, RankRead, StaffUnitRead)


class UserBase(BaseModel):
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    staff_unit_id: Optional[uuid.UUID]
    actual_staff_unit_id: Optional[uuid.UUID]
    icon: Optional[str]
    call_sign: Optional[str]
    id_number: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    birthday: Optional[datetime.date]
    status: Optional[str]
    status_till: Optional[datetime.datetime]
    cabinet: Optional[str]
    service_phone_number: Optional[str]


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserGroupUpdate(BaseModel):
    user_id: uuid.UUID
    group_id: uuid.UUID


class UserRead(UserBase):
    id: Optional[uuid.UUID]
    badges: Optional[List[BadgeRead]]
    staff_unit: Optional[StaffUnitRead]
    actual_staff_unit: Optional[StaffUnitRead]
    rank: Optional[RankRead]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    staff_unit_id: Optional[uuid.UUID]
    call_sign: Optional[str]
    id_number: Optional[str]
    status: Optional[str]
    status_till: Optional[datetime.datetime]
    personal_id: Optional[str]

    class Config:
        orm_mode = True

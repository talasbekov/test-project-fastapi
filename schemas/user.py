import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from schemas import (BadgeRead, RankRead, UserStaffUnitRead)


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
    status: Optional[str]
    status_till: Optional[datetime.datetime]
    cabinet: Optional[str]
    service_phone_number: Optional[str]
    supervised_by: Optional[uuid.UUID]
    is_military: Optional[bool]
    personal_id: Optional[str]


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
    is_military: Optional[bool]
    staff_unit: Optional[UserStaffUnitRead]
    actual_staff_unit: Optional[UserStaffUnitRead]
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
    badges: Optional[List[BadgeRead]]
    staff_unit: Optional[UserStaffUnitRead]
    actual_staff_unit: Optional[UserStaffUnitRead]

    class Config:
        orm_mode = True

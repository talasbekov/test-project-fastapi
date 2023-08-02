import datetime
import uuid
from typing import List, Optional

from pydantic import EmailStr, Field, root_validator, validator

from schemas import (BadgeRead, RankRead, UserStaffUnitRead,
                     StatusRead, ShortUserStaffUnitRead)
from schemas import Model, ReadModel, BaseModel


class UserBase(Model):
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
    cabinet: Optional[str]
    service_phone_number: Optional[str]
    supervised_by: Optional[uuid.UUID]
    is_military: Optional[bool]
    personal_id: Optional[str]
    date_birth: Optional[datetime.date]
    iin: Optional[str]
    is_active: Optional[bool]
    id: Optional[uuid.UUID]
    description: Optional[str]


class UserCreate(UserBase):
    password: Optional[str]

class UserUpdate(UserBase):
    pass


class UserGroupUpdate(Model):
    user_id: uuid.UUID
    group_id: uuid.UUID
    
class UserRead(UserBase, ReadModel):
    badges: Optional[List[BadgeRead]]
    is_military: Optional[bool]
    staff_unit: Optional[ShortUserStaffUnitRead]
    actual_staff_unit: Optional[ShortUserStaffUnitRead]
    rank: Optional[RankRead]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    last_signed_at: Optional[datetime.datetime]
    staff_unit_id: Optional[uuid.UUID]
    call_sign: Optional[str]
    id_number: Optional[str]
    status_till: Optional[datetime.datetime]
    personal_id: Optional[str]
    badges: Optional[List[BadgeRead]]
    date_birth: Optional[datetime.date]
    iin: Optional[str]
    statuses: Optional[List[StatusRead]]

    class Config:
        orm_mode = True

class UserShortRead(Model):
    id: Optional[uuid.UUID]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    icon: Optional[str]
    rank: Optional[RankRead]


    class Config:
        orm_mode = True


class UserShortReadStatus(Model):
    id: Optional[uuid.UUID]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    icon: Optional[str]
    rank: Optional[RankRead]
    statuses: Optional[List[StatusRead]]


    class Config:
        orm_mode = True


class TableUserRead(Model):
    total: int
    users: List[UserRead]


class UserShortReadStatusPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[UserShortReadStatus] = Field([], nullable=False)
import datetime
import uuid
from typing import List, Optional
from dateutil.relativedelta import relativedelta

from pydantic import EmailStr, Field, root_validator, validator

from schemas import (BadgeRead, RankRead, UserStaffUnitRead,
                     StatusRead, ShortUserStaffUnitRead)
from schemas import Model, ReadModel, BaseModel

def calculate_age_from_birthdate(birth_date):
    today = datetime.datetime.now()
    age = relativedelta(today, birth_date)
    return age.years


def get_age_group(age):
    if age <= 25:
        return 1
    elif age < 30:
        return 2
    elif age < 35:
        return 3
    elif age < 40:
        return 4
    elif age < 45:
        return 5
    elif age < 50:
        return 6
    else:
        return 0

class UserBase(Model):
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    staff_unit_id: Optional[str]
    actual_staff_unit_id: Optional[str]
    icon: Optional[str]
    call_sign: Optional[str]
    id_number: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    cabinet: Optional[str]
    service_phone_number: Optional[str]
    supervised_by: Optional[str]
    is_military: Optional[bool]
    personal_id: Optional[str]
    date_birth: Optional[datetime.date]
    iin: Optional[str]
    is_active: Optional[bool]
    id: Optional[str]
    description: Optional[str]


class UserCreate(UserBase):
    password: Optional[str]

class UserUpdate(UserBase):
    pass


class UserGroupUpdate(Model):
    user_id: str
    group_id: str
    
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
    staff_unit_id: Optional[str]
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
    id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    icon: Optional[str]
    rank: Optional[RankRead]


    class Config:
        orm_mode = True

class UserShortReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[UserShortRead] = Field([], nullable=False)

class UserShortReadStatus(Model):
    id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    icon: Optional[str]
    rank: Optional[RankRead]
    statuses: Optional[List[StatusRead]]


    class Config:
        orm_mode = True


class UserShortReadAgeCategory(Model):
    id: Optional[uuid.UUID]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    icon: Optional[str]
    rank: Optional[RankRead]
    date_birth: Optional[datetime.date]
    staff_division: Optional[dict]
    age_category: Optional[int]

    @classmethod
    def from_orm(cls, orm_obj):
        staff_division = orm_obj.staff_unit.staff_division
        age = calculate_age_from_birthdate(orm_obj.date_birth)
        return cls(
            id=orm_obj.id,
            first_name=orm_obj.first_name,
            last_name=orm_obj.last_name,
            father_name=orm_obj.father_name,
            icon=orm_obj.icon,
            rank=orm_obj.rank,
            date_birth=orm_obj.date_birth,
            staff_division={"name": staff_division.name
                                   if staff_division else None,
                            "nameKZ": staff_division.nameKZ
                                   if staff_division else None
                            },
            age_category=get_age_group(age)
        )

    class Config:
        orm_mode = True


class TableUserRead(Model):
    total: int
    users: List[UserRead]


class UserShortReadStatusPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[UserShortReadStatus] = Field([], nullable=False)
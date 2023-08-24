import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, validator

from schemas import (BadgeRead, RankRead, ReadModel,
                     StaffUnitHrVacancyRead, Model, PositionRead)

from .archive_staff_function import ArchiveStaffFunctionRead


class StaffUnitRequirements(Model):
    name: Optional[str]
    nameKZ: Optional[str]
    keys: Optional[List[Optional[dict]]]


class ArchiveStaffUnitBase(BaseModel):
    position_id: str
    staff_division_id: str
    user_id: Optional[str] = Field(None, nullable=True)
    actual_user_id: Optional[str] = Field(None, nullable=True)
    user_replacing_id: Optional[str] = Field(None, nullable=True)
    requirements: Optional[List[StaffUnitRequirements]]


class ArchiveStaffUnitCreate(ArchiveStaffUnitBase):
    curator_of_id: Optional[str] = Field(None, nullable=True)
    origin_id: Optional[str] = Field(None, nullable=True)
    requirements: Optional[str]


class ArchiveStaffUnitCreateWithStaffFunctions(ArchiveStaffUnitBase):
    origin_id: Optional[str]
    staff_functions: Optional[List[ArchiveStaffFunctionRead]]


class ArchiveStaffUnitUpdate(ArchiveStaffUnitBase):
    origin_id: Optional[str]
    user_replacing: Optional[str] = Field(None, nullable=True)
    curator_of_id: Optional[str] = Field(None, nullable=True)


class NewArchiveStaffUnitCreate(ArchiveStaffUnitBase):
    curator_of_id: Optional[str] = Field(None, nullable=True)
    @validator('user_replacing_id')
    def validate_user_replacing_id(cls, user_replacing_id, values):
        user_id = values.get('user_id')
        if user_replacing_id is not None and user_id is not None:
            if user_replacing_id == user_id:
                raise ValueError("user_replacing_id cannot be equal to user_id")
        return user_replacing_id
    pass


class NewArchiveStaffUnitCreateWithStaffFunctions(ArchiveStaffUnitBase):
    staff_functions: Optional[List[ArchiveStaffFunctionRead]]


class NewArchiveStaffUnitUpdate(ArchiveStaffUnitBase):
    curator_of_id: Optional[str] = Field(None, nullable=True)

    @validator('user_replacing_id')
    def validate_user_replacing_id(cls, user_replacing_id, values):
        user_id = values.get('user_id')
        if user_replacing_id is not None and user_id is not None:
            if user_replacing_id == user_id:
                raise ValueError("user_replacing_id cannot be equal to user_id")
        return user_replacing_id
    pass


class ArchiveStaffUnitUpdateDispose(BaseModel):
    staff_unit_ids: List[str]
    staff_list_id: str


class UserRead(BaseModel):
    id: Optional[str]
    badges: Optional[List[BadgeRead]]
    rank: Optional[RankRead]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    staff_unit_id: Optional[str]
    call_sign: Optional[str]
    id_number: Optional[str]
    status: Optional[str]
    status_till: Optional[datetime.datetime]
    icon: Optional[str]
    is_military: Optional[bool]

    class Config:
        orm_mode = True



class UserReplacingArchiveStaffUnitRead(ArchiveStaffUnitBase, ReadModel):
    id: Optional[str]
    staff_division_id: Optional[str]
    staff_functions: Optional[List[ArchiveStaffFunctionRead]]
    position_id: Optional[str]
    position: Optional[PositionRead]
    user: Optional[UserRead] = Field(None, nullable=True)
    actual_user: Optional[UserRead] = Field(None, nullable=True)
    hr_vacancy: Optional[List[Optional[StaffUnitHrVacancyRead]]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserReplacingRead(UserRead):
    staff_unit: Optional[UserReplacingArchiveStaffUnitRead]

    class Config:
        arbitrary_types_allowed = True


class ArchiveStaffUnitRead(UserReplacingArchiveStaffUnitRead):
    user_replacing: Optional[UserReplacingRead] = Field(None, nullable=True)

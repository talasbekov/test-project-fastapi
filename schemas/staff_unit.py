import datetime
import uuid
import json
from typing import List, Optional, Any

from pydantic import EmailStr, Field, validator

from schemas import (BadgeRead, PositionRead, PositionCreate,
                     RankRead, StaffUnitDivisionRead,
                     StaffFunctionRead, ShortStaffUnitDivisionRead)
from schemas import Model, ReadModel, NamedModel


class StaffUnitRequirements(NamedModel):
    keys: Optional[List[Optional[dict]]] = Field(None, nullable=True)
    
    
class StaffUnitBase(Model):
    position_id: str
    staff_division_id: Optional[str] = Field(None, nullable=True)
    is_active: Optional[bool] = True
    requirements: Optional[List[StaffUnitRequirements]
                           ] = Field(None, nullable=True)


class StaffUnitCreate(StaffUnitBase):
    curator_of_id: Optional[str] = Field(None, nullable=True)
    
class StaffUnitFromArchiveCreate(StaffUnitBase):
    curator_of_id: Optional[str] = Field(None, nullable=True)
    requirements: Optional[str]

class StaffUnitCreateWithPosition(PositionCreate):
    staff_division_id: str
    is_active: Optional[bool] = True
    requirements: Optional[List[dict]] = Field(None, nullable=True)


class StaffUnitUpdate(StaffUnitBase):
    requirements: Optional[Any] = Field(None, nullable=True)
    curator_of_id: Optional[str] = Field(None, nullable=True)
    user_replacing_id: Optional[str] = Field(None, nullable=True)


class HrVacancyRead(ReadModel):
    is_active: Optional[bool] = True
    staff_unit_id: Optional[str]

    class Config:
        orm_mode = True


class StaffUnitReadWithoutUser(StaffUnitBase, ReadModel):
    staff_division_id: Optional[str]
    staff_division: Optional[StaffUnitDivisionRead]
    staff_functions: Optional[List[StaffFunctionRead]]
    position_id: Optional[str]
    position: Optional[PositionRead]
    hr_vacancy: Optional[List[Optional[HrVacancyRead]]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserRead(ReadModel):
    badges: Optional[List[BadgeRead]]
    rank: Optional[RankRead]
    email: Optional[EmailStr] = Field(None, nullable=True)
    first_name: Optional[str] = Field(None, nullable=True)
    last_name: Optional[str] = Field(None, nullable=True)
    staff_unit_id: Optional[str]
    call_sign: Optional[str]
    id_number: Optional[str]
    icon: Optional[str] = Field(None, nullable=True)
    status: Optional[str]
    status_till: Optional[datetime.datetime]
    actual_staff_unit_id: Optional[str]
    actual_staff_unit: Optional[StaffUnitReadWithoutUser]

    class Config:
        orm_mode = True


class UserReplacingStaffUnitRead(StaffUnitBase, ReadModel):
    staff_division_id: Optional[str]
    staff_division: Optional[StaffUnitDivisionRead]
    staff_functions: Optional[List[StaffFunctionRead]]
    position_id: Optional[str]
    position: Optional[PositionRead]
    users: Optional[List[Optional[UserRead]]]
    actual_users: Optional[List[Optional[UserRead]]]
    hr_vacancy: Optional[List[Optional[HrVacancyRead]]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserReplacingRead(UserRead):
    staff_unit: Optional[UserReplacingStaffUnitRead]

    class Config:
        arbitrary_types_allowed = True


class StaffUnitRead(UserReplacingStaffUnitRead):
    user_replacing: Optional[UserReplacingRead] = Field(None, nullable=True)
    user_replacing_id: Optional[str] = Field(None, nullable=True)


class UserStaffUnitRead(StaffUnitBase, ReadModel):
    staff_division_id: Optional[str]
    staff_division: Optional[ShortStaffUnitDivisionRead]
    staff_functions: Optional[List[StaffFunctionRead]]
    position_id: Optional[str]
    position: Optional[PositionRead]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class ShortUserStaffUnitRead(ReadModel):
    is_active: Optional[bool] = True
    staff_division_id: Optional[str]
    staff_division: Optional[ShortStaffUnitDivisionRead]
    position_id: Optional[str]
    position: Optional[PositionRead]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
    
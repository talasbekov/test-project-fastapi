import datetime
import uuid
import json
from typing import List, Optional, Any

from pydantic import EmailStr, Field, validator

from schemas import (BadgeRead, PositionRead, PositionCreate,
                     RankRead, StaffUnitDivisionRead,
                     StaffFunctionRead, ShortStaffUnitDivisionRead, SuperShortStaffUnitDivisionRead)
from schemas import Model, ReadModel, NamedModel


class StaffUnitRequirements(NamedModel):
    keys: Optional[List[Optional[dict]]] = Field(None, nullable=True)
    
    
class StaffUnitBase(Model):
    position_id: Optional[str]
    staff_division_id: Optional[str] = Field(None, nullable=True)
    is_active: Optional[bool] = True
    requirements: Optional[Any]


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
    # position_id: Optional[str] = Field(None, nullable=True)
    # actual_position_id: Optional[str] = Field(None, nullable=True)

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
    actual_position_id: Optional[str]
    actual_position: Optional[PositionRead]
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
    father_name: Optional[str]
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
    requirements: Optional[Any]
    position_id: Optional[str]
    position: Optional[PositionRead]
    actual_position_id: Optional[str]
    actual_position: Optional[PositionRead]
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
    actual_position_id: Optional[str]
    actual_position: Optional[PositionRead]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class ShortUserStaffUnitRead(ReadModel):
    is_active: Optional[bool] = True
    staff_division_id: Optional[str]
    staff_division: Optional[ShortStaffUnitDivisionRead]
    position_id: Optional[str]
    position: Optional[PositionRead]
    actual_position_id: Optional[str]
    actual_position: Optional[PositionRead]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
    
class StaffUnitReadActive(ReadModel):
    is_active: Optional[bool] = True
    staff_division_id: Optional[str]
    staff_division: Optional[SuperShortStaffUnitDivisionRead]
    position_id: Optional[str]
    position: Optional[PositionRead]
    actual_position_id: Optional[str]
    actual_position: Optional[PositionRead]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class StaffUnitUpdateOverwrite(Model):
    staff_division_id: Optional[str] = Field(None, nullable=True)
    position_id: Optional[str] = Field(None, nullable=True)
    actual_position_id: Optional[str] = Field(None, nullable=True)
    id: Optional[str]
    rank_id: Optional[str]
    # user_id: Optional[str]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

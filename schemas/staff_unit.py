import datetime
import uuid
from typing import List, Optional

from pydantic import EmailStr, Field

from schemas import (BadgeRead, PositionRead, PositionCreate,
                     RankRead, StaffUnitDivisionRead,
                     StaffFunctionRead)
from schemas import Model, ReadModel, NamedModel


class StaffUnitRequirements(NamedModel):
    keys: Optional[List[Optional[dict]]] = Field(None, nullable=True)


class StaffUnitBase(Model):
    position_id: uuid.UUID
    staff_division_id: Optional[uuid.UUID] = Field(None, nullable=True)
    is_active: Optional[bool] = True
    requirements: Optional[List[StaffUnitRequirements]] = Field(None, nullable=True)


class StaffUnitCreate(StaffUnitBase):
    pass


class StaffUnitCreateWithPosition(PositionCreate):
    staff_division_id: uuid.UUID
    is_active: Optional[bool] = True
    requirements: Optional[List[dict]] = Field(None, nullable=True)


class StaffUnitUpdate(StaffUnitBase):
    user_replacing_id: Optional[uuid.UUID] = Field(None, nullable=True)


class HrVacancyRead(ReadModel):
    is_active: Optional[bool] = True
    staff_unit_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True


class UserRead(ReadModel):
    badges: Optional[List[BadgeRead]]
    rank: Optional[RankRead]
    email: Optional[EmailStr] = Field(None, nullable=True)
    first_name: Optional[str] = Field(None, nullable=True)
    last_name: Optional[str] = Field(None, nullable=True)
    staff_unit_id: Optional[uuid.UUID]
    call_sign: Optional[str]
    id_number: Optional[str]
    icon: Optional[str] = Field(None, nullable=True)
    status: Optional[str]
    status_till: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class UserReplacingStaffUnitRead(StaffUnitBase, ReadModel):
    staff_division_id: Optional[uuid.UUID]
    staff_division: Optional[StaffUnitDivisionRead]
    staff_functions: Optional[List[StaffFunctionRead]]
    position_id: Optional[uuid.UUID]
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
    user_replacing_id: Optional[uuid.UUID] = Field(None, nullable=True)


class UserStaffUnitRead(StaffUnitBase, ReadModel):
    staff_division_id: Optional[uuid.UUID]
    staff_division: Optional[StaffUnitDivisionRead]
    staff_functions: Optional[List[StaffFunctionRead]]
    position_id: Optional[uuid.UUID]
    position: Optional[PositionRead]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

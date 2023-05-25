import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from schemas import (BadgeRead, PositionRead,
                     RankRead, StaffUnitDivisionRead,
                     StaffFunctionRead)
from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class StaffUnitBase(Model):
    position_id: uuid.UUID
    staff_division_id: uuid.UUID
    is_active: Optional[bool] = True
    requirements: Optional[List[dict]]


class StaffUnitCreate(StaffUnitBase):
    pass


class StaffUnitUpdate(StaffUnitBase):
    pass


class UserRead(ReadModel):
    badges: Optional[List[BadgeRead]]
    rank: Optional[RankRead]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    staff_unit_id: Optional[uuid.UUID]
    call_sign: Optional[str]
    id_number: Optional[str]
    icon: Optional[str]
    status: Optional[str]
    status_till: Optional[datetime.datetime]


    class Config:
        orm_mode = True


class HrVacancyRead(ReadModel):
    is_active: Optional[bool]
    staff_unit_id: Optional[uuid.UUID]
    
    class Config:
        orm_mode = True


class StaffUnitRead(StaffUnitBase, ReadModel):
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


class UserStaffUnitRead(StaffUnitBase, ReadModel):
    staff_division_id: Optional[uuid.UUID]
    staff_division: Optional[StaffUnitDivisionRead]
    staff_functions: Optional[List[StaffFunctionRead]]
    position_id: Optional[uuid.UUID]
    position: Optional[PositionRead]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

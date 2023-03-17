import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from schemas import (BadgeRead, PositionRead,
                     RankRead, StaffDivisionRead,
                     StaffFunctionRead)


class StaffUnitBase(BaseModel):
    pass


class StaffUnitCreate(StaffUnitBase):
    pass


class StaffUnitUpdate(StaffUnitBase):
    pass


class UserRead(BaseModel):
    id: Optional[uuid.UUID]
    badges: Optional[List[BadgeRead]]
    rank: Optional[RankRead]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    staff_unit_id: Optional[uuid.UUID]
    call_sign: Optional[str]
    id_number: Optional[str]
    status: Optional[str]
    status_till: Optional[datetime.datetime]


    class Config:
        orm_mode = True


class StaffUnitRead(StaffUnitBase):
    id: Optional[uuid.UUID]
    staff_division_id: Optional[uuid.UUID]
    staff_division: Optional[StaffDivisionRead]
    staff_functions: Optional[List[StaffFunctionRead]]
    position_id: Optional[uuid.UUID]
    position: Optional[PositionRead]
    users: Optional[List[Optional[UserRead]]]
    actual_users: Optional[List[Optional[UserRead]]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

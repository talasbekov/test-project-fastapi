import datetime
import uuid
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr

from schemas import (BadgeRead, PositionRead,
                     RankRead)
from .archive_staff_division import ArchiveStaffDivisionRead
from .archive_staff_function import ArchiveStaffFunctionRead

class ArchiveStaffUnitBase(BaseModel):
    pass


class ArchiveStaffUnitCreate(ArchiveStaffUnitBase):
    pass

class ArchiveStaffUnitCreateWithStaffFunctions(ArchiveStaffUnitBase):
    staff_functions: Optional[List[ArchiveStaffFunctionRead]]


class ArchiveStaffUnitUpdate(ArchiveStaffUnitBase):
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


class ArchiveStaffUnitRead(ArchiveStaffUnitBase):
    id: Optional[uuid.UUID]
    staff_division_id: Optional[uuid.UUID]
    staff_division: Optional[ArchiveStaffDivisionRead]
    staff_functions: Optional[List[ArchiveStaffFunctionRead]]
    position_id: Optional[uuid.UUID]
    position: Optional[PositionRead]
    users: Optional[List[Optional[UserRead]]]
    actual_users: Optional[List[Optional[UserRead]]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

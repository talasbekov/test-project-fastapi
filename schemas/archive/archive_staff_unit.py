import datetime
import uuid
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr

from schemas import BadgeRead, PositionRead, RankRead, ReadModel

from .archive_staff_function import ArchiveStaffFunctionRead


class ArchiveStaffUnitBase(BaseModel):
    position_id: uuid.UUID
    staff_division_id: uuid.UUID
    user_id: Optional[uuid.UUID]
    actual_user_id: Optional[uuid.UUID]
    user_replacing_id: Optional[uuid.UUID]

class ArchiveStaffUnitCreate(ArchiveStaffUnitBase):
    origin_id: Optional[uuid.UUID]


class ArchiveStaffUnitCreateWithStaffFunctions(ArchiveStaffUnitBase):
    origin_id: Optional[uuid.UUID]
    staff_functions: Optional[List[ArchiveStaffFunctionRead]]


class ArchiveStaffUnitUpdate(ArchiveStaffUnitBase):
    origin_id: Optional[uuid.UUID]


class NewArchiveStaffUnitCreate(ArchiveStaffUnitBase):
    pass


class NewArchiveStaffUnitCreateWithStaffFunctions(ArchiveStaffUnitBase):
    staff_functions: Optional[List[ArchiveStaffFunctionRead]]


class NewArchiveStaffUnitUpdate(ArchiveStaffUnitBase):
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

class UserReplacingArchiveStaffUnitRead(ArchiveStaffUnitBase, ReadModel):
    id: Optional[uuid.UUID]
    staff_division_id: Optional[uuid.UUID]
    staff_functions: Optional[List]
    position_id: Optional[uuid.UUID]
    position: Optional[PositionRead]
    user: Optional[UserRead]
    actual_user: Optional[UserRead]
    #hr_vacancy: Optional[List[Optional[HrVacancyRead]]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UserReplacingRead(UserRead):
    staff_unit: Optional[UserReplacingArchiveStaffUnitRead]
    
    class Config:
        arbitrary_types_allowed = True


class ArchiveStaffUnitRead(UserReplacingArchiveStaffUnitRead):
    user_replacing: Optional[UserReplacingRead]
    

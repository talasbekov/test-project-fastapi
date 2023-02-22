import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from .badge import BadgeRead
from .permission import PermissionRead
from .staff_unit import StaffUnitRead
from .rank import RankRead
from .staff_division import StaffDivisionRead


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    father_name: Optional[str]
    group_id: uuid.UUID
    position_id: uuid.UUID
    icon: Optional[str]
    call_sign: str
    id_number: str
    phone_number: Optional[str]
    address: Optional[str]
    birthday: Optional[datetime.date]
    status: Optional[str]
    status_till: Optional[datetime.datetime]


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: Optional[uuid.UUID]
    badges: Optional[List[BadgeRead]]
    position: Optional[StaffUnitRead]
    actual_position:Optional[StaffUnitRead]
    group: Optional[StaffDivisionRead]
    rank: Optional[RankRead]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    group_id: Optional[uuid.UUID]
    position_id: Optional[uuid.UUID]
    call_sign: Optional[str]
    id_number: Optional[str]
    status: Optional[str]
    status_till: Optional[datetime.datetime]
    permissions: Optional[List[PermissionRead]]

    class Config:
        orm_mode = True

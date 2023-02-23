import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from .badge import BadgeRead
from .permission import PermissionRead
from .rank import RankRead
from .staff_division import StaffDivisionRead
from .staff_unit import StaffUnitRead


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    father_name: Optional[str]
    staff_division_id: uuid.UUID
    staff_unit_id: uuid.UUID
    actual_staff_unit_id: uuid.UUID
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
    staff_unit: Optional[StaffUnitRead]
    actual_staff_unit:Optional[StaffUnitRead]
    staff_division: Optional[StaffDivisionRead]
    rank: Optional[RankRead]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    staff_division_id: Optional[uuid.UUID]
    staff_unit_id: Optional[uuid.UUID]
    call_sign: Optional[str]
    id_number: Optional[str]
    status: Optional[str]
    status_till: Optional[datetime.datetime]
    permissions: Optional[List[PermissionRead]]

    class Config:
        orm_mode = True

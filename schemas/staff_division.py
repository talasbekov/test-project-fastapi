import datetime
import uuid
from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr

from schemas import PositionRead, RankRead


class StaffDivisionBase(BaseModel):
    parent_group_id: Optional[uuid.UUID]
    name: str
    description: Optional[str]


class StaffDivisionCreate(StaffDivisionBase):
    pass


class StaffDivisionUpdate(StaffDivisionBase):
    pass


class StaffDivisionUpdateParentGroup(BaseModel):
    parent_group_id: uuid.UUID


class StaffDivisionRead(StaffDivisionBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    children: Optional[List['StaffDivisionRead']]

    class Config:
        orm_mode = True


class UserRead(BaseModel):
    id: Optional[uuid.UUID]
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


class StaffUnitOptionRead(BaseModel):

    id: Optional[uuid.UUID]
    position_id: Optional[uuid.UUID]
    position: Optional[PositionRead]
    users: Optional[List[Optional[UserRead]]]
    actual_users: Optional[List[Optional[UserRead]]]

    class Config:
        orm_mode = True


class StaffDivisionOptionRead(StaffDivisionBase):

    id: Optional[uuid.UUID]
    name: Optional[str]
    children: Optional[List['StaffDivisionRead']]
    staff_units: Optional[List[StaffUnitOptionRead]]

    class Config:
        orm_mode = True

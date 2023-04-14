import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from schemas import PositionRead, RankRead
from schemas import Model, NamedModel, ReadModel, ReadNamedModel



class StaffDivisionBase(NamedModel):
    parent_group_id: Optional[uuid.UUID]
    description: Optional[str]
    is_combat_unit: bool
    leader_id: Optional[uuid.UUID]


class StaffDivisionCreate(StaffDivisionBase):
    pass


class StaffDivisionUpdate(StaffDivisionBase):
    pass


class StaffDivisionUpdateParentGroup(BaseModel):
    parent_group_id: uuid.UUID


class StaffDivisionRead(StaffDivisionBase, ReadNamedModel):
    is_combat_unit: Optional[bool]
    children: Optional[List['StaffDivisionRead']]
    staff_units: Optional[List]

    class Config:
        orm_mode = True


class UserRead(ReadModel):
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


class StaffUnitRead(ReadModel):
    staff_division_id: Optional[uuid.UUID]
    position_id: Optional[uuid.UUID]
    position: Optional[PositionRead]
    users: Optional[List[Optional[UserRead]]]
    actual_users: Optional[List[Optional[UserRead]]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StaffDivisionOptionRead(StaffDivisionBase, ReadNamedModel):
    is_combat_unit: Optional[bool]
    staff_units: Optional[List[StaffUnitRead]]
    children: Optional[List['StaffDivisionOptionRead']]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StaffUnitDivisionRead(StaffDivisionBase, ReadNamedModel):
    is_combat_unit: Optional[bool]

    class Config:
        orm_mode = True

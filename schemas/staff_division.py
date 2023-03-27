import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from schemas import PositionRead, RankRead


class StaffDivisionBase(BaseModel):
    parent_group_id: Optional[uuid.UUID]
    name: str
    description: Optional[str]
    is_combat_unit: bool


class StaffDivisionCreate(StaffDivisionBase):
    pass


class StaffDivisionUpdate(StaffDivisionBase):
    pass


class StaffDivisionUpdateParentGroup(BaseModel):
    parent_group_id: uuid.UUID


class StaffDivisionRead(StaffDivisionBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    is_combat_unit: Optional[bool]
    children: Optional[List['StaffDivisionRead']]
    staff_units: Optional[List]

    class Config:
        orm_mode = True


class StaffDivisionOptionRead(StaffDivisionBase):

    id: Optional[uuid.UUID]
    name: Optional[str]
    staff_units: Optional[List]
    children: Optional[List['StaffDivisionOptionRead']]

    class Config:
        orm_mode = True

class StaffUnitDivisionRead(StaffDivisionBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    is_combat_unit: Optional[bool]

    class Config:
        orm_mode = True

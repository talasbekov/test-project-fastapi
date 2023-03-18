import datetime
import uuid
from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr

from schemas import PositionRead, RankRead


class ArchiveStaffDivisionBase(BaseModel):
    parent_group_id: Optional[uuid.UUID]
    name: str
    description: Optional[str]
    staff_list_id: uuid.UUID
    origin_id: Optional[uuid.UUID]


class ArchiveStaffDivisionCreate(ArchiveStaffDivisionBase):
    pass


class ArchiveStaffDivisionUpdate(ArchiveStaffDivisionBase):
    pass


class ArchiveStaffDivisionUpdateParentGroup(BaseModel):
    parent_group_id: uuid.UUID


class ArchiveStaffDivisionRead(ArchiveStaffDivisionBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    children: Optional[List['ArchiveStaffDivisionRead']]
    staff_units: Optional[List]

    class Config:
        orm_mode = True


class StaffDivisionOptionRead(ArchiveStaffDivisionBase):

    id: Optional[uuid.UUID]
    name: Optional[str]
    staff_units: Optional[List]
    children: Optional[List['StaffDivisionOptionRead']]

    class Config:
        orm_mode = True

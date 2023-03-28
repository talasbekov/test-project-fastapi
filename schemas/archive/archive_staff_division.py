import uuid
from typing import List, Optional

from pydantic import BaseModel


class ArchiveStaffDivisionBase(BaseModel):
    parent_group_id: Optional[uuid.UUID]
    name: str
    description: Optional[str]
    staff_list_id: uuid.UUID


class ArchiveStaffDivisionCreate(ArchiveStaffDivisionBase):
    origin_id: Optional[uuid.UUID]


class ArchiveStaffDivisionUpdate(ArchiveStaffDivisionBase):
    origin_id: Optional[uuid.UUID]


class NewArchiveStaffDivisionCreate(ArchiveStaffDivisionBase):
    pass


class NewArchiveStaffDivisionUpdate(ArchiveStaffDivisionBase):
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

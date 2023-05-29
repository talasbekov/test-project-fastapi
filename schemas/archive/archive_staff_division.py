import uuid
from typing import List, Optional

from pydantic import BaseModel
from schemas import NamedModel
from .archive_staff_unit import ArchiveStaffUnitRead



class ArchiveStaffDivisionBase(BaseModel):
    parent_group_id: Optional[uuid.UUID]
    name: str
    nameKZ: Optional[str]
    description: Optional[NamedModel]
    staff_list_id: uuid.UUID
    is_combat_unit: Optional[bool]
    leader_id: Optional[uuid.UUID]


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
    children: Optional[List['ArchiveStaffDivisionRead']]
    staff_units: Optional[List['ArchiveStaffUnitRead']]

    class Config:
        orm_mode = True

import uuid
from typing import List, Optional

from pydantic import BaseModel, Field
from schemas import NamedModel, StaffDivisionTypeRead
from .archive_staff_unit import ArchiveStaffUnitRead


class ArchiveStaffDivisionBase(NamedModel):
    parent_group_id: Optional[uuid.UUID] = Field(None, nullable=True)
    description: Optional[NamedModel]
    staff_list_id: uuid.UUID
    is_combat_unit: Optional[bool] = Field(None, nullable=True)
    leader_id: Optional[uuid.UUID] = Field(None, nullable=True)
    type_id: Optional[uuid.UUID] = Field(None, nullable=True)
    staff_division_number: Optional[int] = Field(None, nullable=True)


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


# class ArchiveStaffDivisionRead(ArchiveStaffDivisionBase):
#     id: Optional[uuid.UUID]
#     children: Optional[List['ArchiveStaffDivisionRead']]
#     staff_units: Optional[List['ArchiveStaffUnitRead']]
#     type: Optional[StaffDivisionTypeRead]
#
#     class Config:
#         orm_mode = True


class ArchiveStaffDivisionChildRead(ArchiveStaffDivisionBase):
    id: Optional[uuid.UUID]
    type: Optional[StaffDivisionTypeRead]

    class Config:
        orm_mode = True


class ArchiveStaffDivisionRead(ArchiveStaffDivisionBase):
    id: Optional[uuid.UUID]
    children: Optional[List['ArchiveStaffDivisionChildRead']]
    staff_units: Optional[List['ArchiveStaffUnitRead']]
    type: Optional[StaffDivisionTypeRead]

    class Config:
        orm_mode = True

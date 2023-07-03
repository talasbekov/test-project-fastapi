import uuid
from typing import List, Optional

from pydantic import BaseModel, Field, validator
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
    children: Optional[List]
    staff_units: Optional[List]
    type: Optional[StaffDivisionTypeRead]
    
    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return []
        
    @validator('staff_units')
    def validate_staff_units(cls, staff_units):
        if staff_units == []:
            return None
        else:
            return []

    class Config:
        orm_mode = True


class ArchiveStaffDivisionRead(ArchiveStaffDivisionBase):
    id: Optional[uuid.UUID]
    children: Optional[List['ArchiveStaffDivisionChildRead']]
    staff_units: Optional[List['ArchiveStaffUnitRead']]
    type: Optional[StaffDivisionTypeRead]
    
    @validator('children')
    def validate_children(cls, children):
        if children == []:
            return None
        else:
            return children
        
    @validator('staff_units')
    def validate_staff_units(cls, staff_units):
        if staff_units == []:
            return None
        else:
            return staff_units

    class Config:
        orm_mode = True

class ArchiveStaffDivisionStepChildRead(ArchiveStaffDivisionBase):
    id: Optional[uuid.UUID]
    type: Optional[StaffDivisionTypeRead]

    class Config:
        orm_mode = True

class ArchiveStaffDivisionStepRead(ArchiveStaffDivisionBase):
    id: Optional[uuid.UUID]
    children: Optional[List['ArchiveStaffDivisionStepChildRead']]
    staff_units: Optional[List['ArchiveStaffUnitRead']]
    type: Optional[StaffDivisionTypeRead]

    class Config:
        orm_mode = True

import uuid
from typing import Any, List, Optional

from pydantic import BaseModel


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

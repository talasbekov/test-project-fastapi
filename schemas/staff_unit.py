import uuid
from typing import List, Optional

from pydantic import BaseModel

from schemas import (DocumentStaffFunctionRead, PositionRead,
                     ServiceStaffFunctionRead, StaffDivisionRead,
                     StaffFunctionRead)


class StaffUnitBase(BaseModel):
    max_rank_id: uuid.UUID


class StaffUnitCreate(StaffUnitBase):
    pass


class StaffUnitUpdate(StaffUnitBase):
    pass


class StaffUnitRead(StaffUnitBase):
    id: Optional[uuid.UUID]
    max_rank_id: Optional[uuid.UUID]
    staff_division_id: Optional[uuid.UUID]
    staff_division: Optional[StaffDivisionRead]
    staff_functions: Optional[List[StaffFunctionRead]]
    position_id: Optional[uuid.UUID]
    position: Optional[PositionRead]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

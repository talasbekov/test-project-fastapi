import uuid
from typing import Optional, List

from pydantic import BaseModel

from schemas import ServiceStaffFunctionRead, DocumentStaffFunctionRead


class StaffUnitBase(BaseModel):
    name: str
    max_rank_id: uuid.UUID


class StaffUnitCreate(StaffUnitBase):
    pass


class StaffUnitUpdate(StaffUnitBase):
    pass


class StaffUnitRead(StaffUnitBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    max_rank_id: Optional[uuid.UUID]
    service_staff_functions: Optional[ServiceStaffFunctionRead]
    document_staff_functions: Optional[DocumentStaffFunctionRead]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

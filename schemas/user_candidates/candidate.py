import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class CandidateBase(BaseModel):
    candidate_stage_id: Optional[uuid.UUID] 
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateUserRead(BaseModel):
    id: uuid.UUID
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    icon: Optional[str]

    class Config:
        orm_mode = True

class StaffUnitCandidateRead(BaseModel):
    id: uuid.UUID
    users: Optional[List[CandidateUserRead]] = None


    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
         

class CandidateCreate(CandidateBase):
    staff_unit_curator_id: Optional[uuid.UUID]
    staff_unit_id: Optional[uuid.UUID]


class CandidateUpdate(CandidateBase):
    staff_unit_curator_id: Optional[uuid.UUID]
    staff_unit_id: Optional[uuid.UUID]



class CandidateRead(CandidateBase):
    id: uuid.UUID
    progress: Optional[int]
    current_stage: Optional[uuid.UUID]
    last_edit_date: Optional[datetime]
    staff_unit_curator: Optional[StaffUnitCandidateRead]
    staff_unit: Optional[StaffUnitCandidateRead]

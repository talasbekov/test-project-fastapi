import uuid
import datetime

from typing import Optional, List

from pydantic import BaseModel

from .candidate_stage_info import CandidateStageInfoRead


class CandidateBase(BaseModel):
    staff_unit_curator_id: uuid.UUID
    staff_unit_id: uuid.UUID

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
    pass


class CandidateUpdate(CandidateBase):
    pass


class CandidateRead(CandidateBase):
    id: Optional[uuid.UUID]
    progress: Optional[int]
    current_stage: Optional[uuid.UUID]
    last_edit_date: Optional[datetime.date]
    staff_unit_curator_id: Optional[uuid.UUID]
    staff_unit_curator: Optional[StaffUnitCandidateRead]
    staff_unit_id: Optional[uuid.UUID]
    staff_unit: Optional[StaffUnitCandidateRead]
    candidate_stage_infos: Optional[List[CandidateStageInfoRead]]

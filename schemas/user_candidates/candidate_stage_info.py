import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from .candidate_stage_type import CandidateStageTypeRead
from .candidate import CandidateRead
from .. import Model


class CandidateStageInfoBase(Model):
    candidate_id: str
    candidate_stage_type_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageInfoCreate(CandidateStageInfoBase):
    pass


class CandidateStageInfoSignEcp(Model):
    certificate_blob: str


class CandidateStageInfoUpdate(CandidateStageInfoBase):
    candidate_id: Optional[str]
    candidate_stage_type_id: Optional[str]
    status: Optional[str]


class CandidateStageInfoSendToApproval(Model):
    staff_unit_coordinate_id: Optional[str]


class CandidateStageInfoRead(CandidateStageInfoBase):
    id: Optional[str]
    access: Optional[bool]
    status: Optional[str]
    candidate_id: Optional[str]
    candidate: Optional[CandidateRead]
    is_waits: Optional[bool]
    candidate_stage_type_id: Optional[str]
    candidate_stage_type: Optional[CandidateStageTypeRead]
    date_sign: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

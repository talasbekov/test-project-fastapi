import uuid, datetime
from typing import Optional

from pydantic import BaseModel


class CandidateEssayTypeBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateEssayTypeCreate(CandidateEssayTypeBase):
    pass


class CandidateEssayTypeUpdate(CandidateEssayTypeBase):
    pass


class CandidateEssayTypeSetToCandidate(BaseModel):
    """
        This class is used for set essay_id to candidate

        If candidate chooses from existing essay types then you can set id of essay
        If candidate creates a new essay you can set name of the new essay
    """
    id: Optional[uuid.UUID]
    name: Optional[str]


class CandidateEssayTypeRead(CandidateEssayTypeBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

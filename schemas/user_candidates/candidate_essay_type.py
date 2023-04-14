import uuid, datetime
from typing import Optional

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class CandidateEssayTypeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateEssayTypeCreate(CandidateEssayTypeBase):
    pass


class CandidateEssayTypeUpdate(CandidateEssayTypeBase):
    pass


class CandidateEssayTypeSetToCandidate(NamedModel):
    """
        This class is used for set essay_id to candidate

        If candidate chooses from existing essay types then you can set id of essay
        If candidate creates a new essay you can set name of the new essay
    """
    id: Optional[uuid.UUID]
    name: Optional[str]
    nameKZ: Optional[str]


class CandidateEssayTypeRead(CandidateEssayTypeBase, NamedModel):
    id: Optional[uuid.UUID]

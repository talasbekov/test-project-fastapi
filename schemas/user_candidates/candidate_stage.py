import uuid

from pydantic import BaseModel


class CandidateStageBase(BaseModel):    
    pass

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class CandidateStageCreate(CandidateStageBase):
    pass


class CandidateStageUpdate(CandidateStageBase):
    pass


class CandidateStageRead(CandidateStageBase):
    id: uuid.UUID

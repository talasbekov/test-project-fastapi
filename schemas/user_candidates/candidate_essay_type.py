import uuid
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


class CandidateEssayTypeRead(CandidateEssayTypeBase):
    id: Optional[uuid.UUID]

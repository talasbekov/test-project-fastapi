import uuid
from typing import Optional

from pydantic import BaseModel


class CandidateCategoryBase(BaseModel):
    name: str


class CandidateCategoryCreate(CandidateCategoryBase):
    pass


class CandidateCategoryUpdate(CandidateCategoryBase):
    pass


class CandidateCategoryRead(CandidateCategoryBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True

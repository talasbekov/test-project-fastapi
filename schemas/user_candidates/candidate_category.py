import uuid
import datetime
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
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True

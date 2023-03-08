import uuid
import datetime

from typing import Optional, List

from pydantic import BaseModel


class SportDegreeBase(BaseModel):
    name: str
    assignment_date: datetime.date
    document_link: str
    profile_id: uuid.UUID


class SportDegreeCreate(SportDegreeBase):
    pass


class SportDegreeUpdate(SportDegreeBase):
    pass


class SportDegreeRead(SportDegreeBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    assignment_date: Optional[datetime.date]
    document_link: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True

import uuid
import datetime

from pydantic import BaseModel
from typing import Optional


class AcademicTitleBase(BaseModel):
    profile_id: Optional[uuid.UUID]
    degree_id: Optional[uuid.UUID]
    specialty_id: Optional[uuid.UUID]
    document_number: str
    document_link: str
    assignment_date: Optional[datetime.date]


class AcademicTitleCreate(AcademicTitleBase):
    pass


class AcademicTitleUpdate(AcademicTitleBase):
    pass


class AcademicTitleRead(AcademicTitleBase):
    id: Optional[uuid.UUID]
    profile_id: Optional[uuid.UUID]
    degree_id: Optional[uuid.UUID]
    specialty_id: Optional[uuid.UUID]
    document_number: str
    document_link: str
    assignment_date: Optional[datetime.date]

    class Config:
        orm_mode = True

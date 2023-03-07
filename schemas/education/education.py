import uuid
import datetime

from pydantic import BaseModel
from typing import Optional


class EducationBase(BaseModel):
    name: str
    profile_id: Optional[uuid.UUID]
    institution_id: Optional[uuid.UUID]
    degree_id: str
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: str


class EducationCreate(EducationBase):
    pass


class EducationUpdate(EducationBase):
    pass


class EducationRead(EducationBase):
    id: Optional[uuid.UUID]
    name: str
    profile_id: Optional[uuid.UUID]
    institution_id: Optional[uuid.UUID]
    degree_id: str
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: str

    class Config:
        orm_mode = True

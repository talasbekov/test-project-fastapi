import uuid
import datetime

from pydantic import BaseModel
from typing import Optional

from .institution import InstitutionRead
from .institution_degree_type import InstitutionDegreeTypeRead


class EducationBase(BaseModel):
    profile_id: Optional[uuid.UUID]
    institution_id: Optional[uuid.UUID]
    degree_id: Optional[uuid.UUID]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class EducationCreate(EducationBase):
    pass


class EducationUpdate(EducationBase):
    pass


class EducationRead(EducationBase):
    id: Optional[uuid.UUID]
    profile_id: Optional[uuid.UUID]
    institution_id: Optional[uuid.UUID]
    degree_id: Optional[uuid.UUID]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: str

    institution: Optional[InstitutionRead]
    degree: Optional[InstitutionDegreeTypeRead]

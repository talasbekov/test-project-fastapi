import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, AnyUrl

from .academic_title_degree import AcademicTitleDegreeRead
from .specialty import SpecialtyRead


class AcademicTitleBase(BaseModel):
    profile_id: Optional[str]
    degree_id: Optional[str]
    specialty_id: Optional[str]
    document_number: str
    document_link: Optional[AnyUrl]
    assignment_date: Optional[datetime.date]


class AcademicTitleCreate(AcademicTitleBase):
    pass


class AcademicTitleUpdate(AcademicTitleBase):
    pass


class AcademicTitleRead(AcademicTitleBase):
    id: Optional[str]
    profile_id: Optional[str]
    degree_id: Optional[str]
    specialty_id: Optional[str]
    document_number: str
    document_link: Optional[str]
    assignment_date: Optional[datetime.date]

    degree: Optional[AcademicTitleDegreeRead]
    specialty: Optional[SpecialtyRead]

    class Config:
        orm_mode = True

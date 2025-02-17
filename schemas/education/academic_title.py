import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, AnyUrl

from .academic_title_degree import AcademicTitleDegreeRead
from .specialty import SpecialtyRead

from schemas import NamedModel


class AcademicTitleBase(BaseModel):
    profile_id: Optional[str]
    degree_id: Optional[str]
    specialty_id: Optional[str]
    document_number: Optional[str]
    document_link: Optional[AnyUrl]
    assignment_date: Optional[datetime.date]
    educational_profile_id: Optional[str]


class AcademicTitleCreate(AcademicTitleBase):
    pass


class AcademicTitleUpdate(AcademicTitleBase):
    pass


class AcademicTitleRead(AcademicTitleBase):
    id: Optional[str]
    profile_id: Optional[str]
    degree_id: Optional[str]
    specialty_id: Optional[str]
    document_number: Optional[str]
    document_link: Optional[str]
    assignment_date: Optional[datetime.date]
    educational_profile_id: Optional[str]

    degree: Optional[AcademicTitleDegreeRead]
    specialty: Optional[SpecialtyRead]

    class Config:
        orm_mode = True
        
class AcademicTitleShortRead(BaseModel):
    document_number: str
    document_link: Optional[str]
    assignment_date: Optional[datetime.date]

    degree: Optional[NamedModel]
    specialty: Optional[NamedModel]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

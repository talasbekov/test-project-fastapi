import datetime
from typing import Optional

from pydantic import AnyUrl

from .institution import InstitutionRead
from .specialty import SpecialtyRead
from .institution_degree_type import InstitutionDegreeTypeRead

from schemas import Model, NamedModel


class EducationBase(Model):
    profile_id: Optional[str]
    institution_id: Optional[str]
    degree_id: Optional[str]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: Optional[AnyUrl]
    is_military_school: Optional[bool]
    specialty_id: Optional[str]
    type_of_top: Optional[str]
    document_number: Optional[str]
    date_of_issue: Optional[datetime.date]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class EducationCreate(EducationBase):
    pass


class EducationUpdate(EducationBase):
    pass


class EducationRead(EducationBase):
    id: Optional[str]
    profile_id: Optional[str]
    institution_id: Optional[str]
    degree_id: Optional[str]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: Optional[str]
    specialty: Optional[SpecialtyRead]
    institution: Optional[InstitutionRead]
    degree: Optional[InstitutionDegreeTypeRead]
    
class EducationShortRead(Model):
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: Optional[str]
    specialty: Optional[NamedModel]
    institution: Optional[NamedModel]
    degree: Optional[NamedModel]


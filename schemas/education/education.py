import datetime
from typing import Optional

from pydantic import AnyUrl

from .institution import InstitutionRead
from .specialty import SpecialtyRead
from .institution_degree_type import InstitutionDegreeTypeRead
from .military_institution import MilitaryInstitutionRead

from schemas import Model, NamedModel
from enum import Enum

class SchoolTypeEnum(Enum):
    militaryAcademy = "militaryAcademy"
    fullTime = "fullTime"
    correspondence = "correspondence"

class EducationBase(Model):
    profile_id: Optional[str]
    institution_id: Optional[str]
    military_institution_id: Optional[str]
    degree_id: Optional[str]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: Optional[AnyUrl]
    is_military_school: Optional[bool]
    specialty_id: Optional[str]
    type_of_top: Optional[str]
    document_number: Optional[str]
    date_of_issue: Optional[datetime.date]
    school_type: Optional[str]
    educational_profile_id: Optional[str]
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
    educational_profile_id: Optional[str]
    institution_id: Optional[str]
    military_institution_id: Optional[str]
    degree_id: Optional[str]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: Optional[str]
    specialty: Optional[SpecialtyRead]
    institution: Optional[InstitutionRead]
    degree: Optional[InstitutionDegreeTypeRead]
    school_type: Optional[str]
    military_institution: Optional[MilitaryInstitutionRead]


    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            profile_id=orm_obj.profile_id,
            educational_profile_id=orm_obj.educational_profile_id,
            institution_id=orm_obj.institution_id,
            military_institution_id=orm_obj.military_institution_id,
            degree_id=orm_obj.degree_id,
            start_date=orm_obj.start_date,
            end_date=orm_obj.end_date,
            document_link=orm_obj.document_link,
            specialty=orm_obj.specialty,
            institution=orm_obj.institution,
            degree=orm_obj.degree,
            school_type=orm_obj.school_type,
            military_institution=orm_obj.military_institution,
            date_of_issue=orm_obj.date_of_issue if orm_obj.date_of_issue else orm_obj.start_date,
            is_military_school=False,
        )


class EducationShortRead(Model):
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: Optional[str]
    specialty: Optional[NamedModel]
    institution: Optional[NamedModel]
    degree: Optional[NamedModel]


from datetime import date
from typing import Optional

from pydantic import AnyUrl, BaseModel, validator

from .academic_degree_degree import AcademicDegreeDegreeRead
from .science import ScienceRead
from .specialty import SpecialtyRead

from schemas import NamedModel, Model


class AcademicDegreeBase(Model):
    profile_id: str
    degree_id: str
    science_id: str
    specialty_id: str
    document_number: str
    document_link: Optional[AnyUrl]
    assignment_date: date
    educational_profile_id: Optional[str]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AcademicDegreeCreate(AcademicDegreeBase):
    pass


class AcademicDegreeUpdate(AcademicDegreeBase):
    pass


class AcademicDegreeRead(AcademicDegreeBase):
    id: Optional[str]
    profile_id: Optional[str]
    degree_id: Optional[str]
    science_id: Optional[str]
    specialty_id: Optional[str]
    specialty: Optional[SpecialtyRead]
    document_number: Optional[str]
    document_link: Optional[str]
    assignment_date: Optional[date]
    educational_profile_id: Optional[str]

    degree: Optional[AcademicDegreeDegreeRead]
    science: Optional[ScienceRead]
    specialty: Optional[SpecialtyRead]


class AcademicDegreeShorRead(Model):
    specialty: Optional[NamedModel]
    document_number: Optional[str]
    document_link: Optional[str]
    assignment_date: Optional[date]

    degree: Optional[NamedModel]
    science: Optional[NamedModel]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    # @validator("document_number", "document_link", pre=True, always=True)
    # def default_empty_string(cls, v):
    #     return v if v is not None else "Данные отсутствуют!"
    #
    # @validator("assignment_date", pre=True, always=True)
    # def default_date(cls, v):
    #     return v if v is not None else date(1920, 1, 1)

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            specialty=orm_obj.specialty,
            document_number=orm_obj.document_number,
            document_link=orm_obj.document_link,
            assignment_date=orm_obj.assignment_date,
            degree=orm_obj.degree,
            science=orm_obj.science,
        )
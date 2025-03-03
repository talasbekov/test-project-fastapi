import datetime

from typing import Optional

from pydantic import BaseModel, AnyUrl, validator

from .academic_title_degree import AcademicTitleDegreeRead
from .specialty import SpecialtyRead

from schemas import NamedModel, CustomBaseModel


class AcademicTitleBase(CustomBaseModel):
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
        
class AcademicTitleShortRead(CustomBaseModel):
    document_number: Optional[str] = "Данные отсутствуют!"
    document_link: Optional[str] = "Данные отсутствуют!"
    assignment_date: Optional[datetime.date] = datetime.date(1920, 1, 1)

    degree: Optional[NamedModel] = NamedModel()
    specialty: Optional[NamedModel] = NamedModel()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @validator("document_number", "document_link", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else "Данные отсутствуют!"

    @validator("assignment_date", pre=True, always=True)
    def default_date(cls, v):
        return v if v is not None else datetime.date(1920, 1, 1)

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            document_number=orm_obj.document_number or "Данные отсутствуют!",
            document_link=orm_obj.document_link or "Данные отсутствуют!",
            assignment_date=orm_obj.assignment_date or datetime.date(1920, 1, 1),
            degree=orm_obj.degree if orm_obj.degree else NamedModel(),
            specialty=orm_obj.specialty if orm_obj.specialty else NamedModel(),
        )

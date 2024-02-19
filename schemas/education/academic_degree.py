import uuid
from datetime import date
from typing import Optional

from pydantic import AnyUrl, BaseModel

from .academic_degree_degree import AcademicDegreeDegreeRead
from .science import ScienceRead
from .specialty import SpecialtyRead

from schemas import NamedModel


class AcademicDegreeBase(BaseModel):
    profile_id: str
    degree_id: str
    science_id: str
    specialty_id: str
    document_number: str
    document_link: Optional[AnyUrl]
    assignment_date: date

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

    degree: Optional[AcademicDegreeDegreeRead]
    science: Optional[ScienceRead]
    specialty: Optional[SpecialtyRead]

class AcademicDegreeShorRead(BaseModel):
    specialty: Optional[NamedModel]
    document_number: Optional[str]
    document_link: Optional[str]
    assignment_date: Optional[date]

    degree: Optional[NamedModel]
    science: Optional[NamedModel]
    specialty: Optional[NamedModel]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
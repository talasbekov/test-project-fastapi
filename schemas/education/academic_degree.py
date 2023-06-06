import uuid
from datetime import date
from typing import Optional

from pydantic import AnyUrl, BaseModel

from .academic_degree_degree import AcademicDegreeDegreeRead
from .science import ScienceRead
from .specialty import SpecialtyRead


class AcademicDegreeBase(BaseModel):
    profile_id: uuid.UUID      
    degree_id: uuid.UUID
    science_id: uuid.UUID
    specialty_id: uuid.UUID
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
    id: Optional[uuid.UUID]
    profile_id: Optional[uuid.UUID]
    degree_id: Optional[uuid.UUID]
    science_id: Optional[uuid.UUID]
    specialty_id: Optional[uuid.UUID]
    document_number: Optional[str]
    document_link: Optional[str]
    assignment_date: Optional[date]

    degree: Optional[AcademicDegreeDegreeRead]
    science: Optional[ScienceRead]
    specialty: Optional[SpecialtyRead]

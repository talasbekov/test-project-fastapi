import uuid

from pydantic import BaseModel
from typing import Optional


class AcademicDegreeBase(BaseModel):
    profile_id: Optional[uuid.UUID]
    degree_id: Optional[uuid.UUID]
    science_id: Optional[uuid.UUID]
    specialty_id: Optional[uuid.UUID]
    document_number: str
    document_link: str


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
    document_number: str
    document_link: str

    class Config:
        orm_mode = True

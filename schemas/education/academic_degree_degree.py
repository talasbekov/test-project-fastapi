import uuid

from pydantic import BaseModel
from typing import Optional


class AcademicDegreeDegreeBase(BaseModel):
    name: str


class AcademicDegreeDegreeCreate(AcademicDegreeDegreeBase):
    pass


class AcademicDegreeDegreeUpdate(AcademicDegreeDegreeBase):
    pass


class AcademicDegreeDegreeRead(AcademicDegreeDegreeBase):
    id: Optional[uuid.UUID]
    name: str

    class Config:
        orm_mode = True

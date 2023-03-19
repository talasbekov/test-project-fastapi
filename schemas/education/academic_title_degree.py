import uuid
from typing import Optional

from pydantic import BaseModel


class AcademicTitleDegreeBase(BaseModel):
    name: str


class AcademicTitleDegreeCreate(AcademicTitleDegreeBase):
    pass


class AcademicTitleDegreeUpdate(AcademicTitleDegreeBase):
    pass


class AcademicTitleDegreeRead(AcademicTitleDegreeBase):
    id: Optional[uuid.UUID]
    name: str

    class Config:
        orm_mode = True

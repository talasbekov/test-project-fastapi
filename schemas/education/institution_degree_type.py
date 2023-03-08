import uuid

from pydantic import BaseModel
from typing import Optional


class InstitutionDegreeTypeBase(BaseModel):
    name: str
    InstitutionDegreeType_id: Optional[uuid.UUID]


class InstitutionDegreeTypeCreate(InstitutionDegreeTypeBase):
    pass


class InstitutionDegreeTypeUpdate(InstitutionDegreeTypeBase):
    pass


class InstitutionDegreeTypeRead(InstitutionDegreeTypeBase):
    id: Optional[uuid.UUID]
    name: str
    InstitutionDegreeType_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True

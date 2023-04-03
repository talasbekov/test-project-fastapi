import uuid
from typing import Optional

from pydantic import BaseModel


class InstitutionDegreeTypeBase(BaseModel):
    name: str


class InstitutionDegreeTypeCreate(InstitutionDegreeTypeBase):
    pass


class InstitutionDegreeTypeUpdate(InstitutionDegreeTypeBase):
    pass


class InstitutionDegreeTypeRead(InstitutionDegreeTypeBase):
    id: Optional[uuid.UUID]
    name: str

    class Config:
        orm_mode = True

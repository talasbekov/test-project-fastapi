import uuid
from typing import Optional

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class InstitutionDegreeTypeBase(NamedModel):
    pass


class InstitutionDegreeTypeCreate(InstitutionDegreeTypeBase):
    pass


class InstitutionDegreeTypeUpdate(InstitutionDegreeTypeBase):
    pass


class InstitutionDegreeTypeRead(InstitutionDegreeTypeBase, ReadNamedModel):

    class Config:
        orm_mode = True

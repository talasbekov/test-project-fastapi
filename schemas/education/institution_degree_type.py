from typing import List, Optional
from pydantic import BaseModel
from schemas import NamedModel, ReadNamedModel, CustomBaseModel


class InstitutionDegreeTypeBase(NamedModel):
    pass


class InstitutionDegreeTypeCreate(InstitutionDegreeTypeBase):
    pass


class InstitutionDegreeTypeUpdate(InstitutionDegreeTypeBase):
    pass


class InstitutionDegreeTypeRead(InstitutionDegreeTypeBase, ReadNamedModel):

    class Config:
        orm_mode = True


class InstitutionDegreeTypeReadPagination(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[InstitutionDegreeTypeRead]]
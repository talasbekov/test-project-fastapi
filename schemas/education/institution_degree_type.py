from typing import List, Optional

from schemas import NamedModel, ReadNamedModel, BaseModel


class InstitutionDegreeTypeBase(NamedModel):
    pass


class InstitutionDegreeTypeCreate(InstitutionDegreeTypeBase):
    pass


class InstitutionDegreeTypeUpdate(InstitutionDegreeTypeBase):
    pass


class InstitutionDegreeTypeRead(InstitutionDegreeTypeBase, ReadNamedModel):

    class Config:
        orm_mode = True


class InstitutionDegreeTypeReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[InstitutionDegreeTypeRead]]
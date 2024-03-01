from typing import Optional, List

from schemas import NamedModel, ReadNamedModel, BaseModel


class InstitutionBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class InstitutionCreate(InstitutionBase):
    pass


class InstitutionUpdate(InstitutionBase):
    pass


class InstitutionRead(InstitutionBase, ReadNamedModel):
    pass

class InstitutionReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[InstitutionRead]]
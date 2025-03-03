from typing import Optional, List
from pydantic import BaseModel
from schemas import NamedModel, ReadNamedModel, CustomBaseModel


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

class InstitutionReadPagination(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[InstitutionRead]]
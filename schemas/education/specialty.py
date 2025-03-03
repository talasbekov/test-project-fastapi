from typing import Optional, List
from pydantic import BaseModel
from schemas import NamedModel, ReadNamedModel, CustomBaseModel


class SpecialtyBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SpecialtyCreate(SpecialtyBase):
    pass


class SpecialtyUpdate(SpecialtyBase):
    pass


class SpecialtyRead(SpecialtyBase, ReadNamedModel):
    pass


class SpecialtyReadPagination(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[SpecialtyRead]]

from typing import Optional, List

from schemas import NamedModel, ReadNamedModel, BaseModel


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


class SpecialtyReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[SpecialtyRead]]

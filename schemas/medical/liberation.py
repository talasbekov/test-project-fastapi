from typing import Optional, List
from schemas import NamedModel, ReadNamedModel, CustomBaseModel


class LiberationBase(NamedModel):
    pass


class LiberationCreate(LiberationBase):
    pass


class LiberationUpdate(LiberationBase):
    pass


class LiberationRead(LiberationBase, ReadNamedModel):

    class Config:
        orm_mode = True


class LiberationReadPagination(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[LiberationRead]]
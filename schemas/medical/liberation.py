from typing import Optional, List

from schemas import NamedModel, ReadNamedModel, BaseModel


class LiberationBase(NamedModel):
    pass


class LiberationCreate(LiberationBase):
    pass


class LiberationUpdate(LiberationBase):
    pass


class LiberationRead(LiberationBase, ReadNamedModel):

    class Config:
        orm_mode = True


class LiberationReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[LiberationRead]]
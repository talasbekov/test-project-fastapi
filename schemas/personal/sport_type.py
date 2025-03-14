from schemas import NamedModel, ReadNamedModel, Model
from typing import Optional, List


class SportTypeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SportTypeCreate(SportTypeBase):
    pass


class SportTypeUpdate(SportTypeBase):
    pass


class SportTypeRead(SportTypeBase, ReadNamedModel):
    pass

class SportTypePaginationRead(Model):
    total: Optional[int]
    objects: Optional[List[SportTypeRead]]

from typing import Optional, List
from schemas import NamedModel, ReadNamedModel, Model


class MilitaryUnitBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class MilitaryUnitCreate(MilitaryUnitBase):
    pass


class MilitaryUnitUpdate(MilitaryUnitBase):
    pass


class MilitaryUnitRead(MilitaryUnitBase, ReadNamedModel):
    pass


class MilitaryUnitReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[MilitaryUnitRead]]
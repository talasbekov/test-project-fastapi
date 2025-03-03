from typing import Optional, List
from schemas import NamedModel, ReadNamedModel, CustomBaseModel


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


class MilitaryUnitReadPagination(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[MilitaryUnitRead]]
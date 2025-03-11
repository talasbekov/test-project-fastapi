import uuid

from typing import Optional, List


from schemas import NamedModel, ReadNamedModel
from schemas.base import Model


class PenaltyTypeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PenaltyTypeCreate(PenaltyTypeBase):
    pass


class PenaltyTypeUpdate(PenaltyTypeBase):
    pass


class PenaltyTypeRead(PenaltyTypeBase, ReadNamedModel):
    pass

class PenaltyTypePaginationRead(Model):
    total: Optional[int]
    objects: Optional[List[PenaltyTypeRead]]

class PenaltyBase(Model):
    user_id: str
    type_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PenaltyCreate(PenaltyBase):
    pass


class PenaltyUpdate(PenaltyBase):
    user_id: Optional[str]
    type_id: Optional[str]


class PenaltyRead(PenaltyBase):
    id: str
    type: Optional[PenaltyTypeRead]


class PenaltyPaginationRead(Model):
    total: Optional[int]
    objects: Optional[List[PenaltyRead]]


class PenaltyReadForOption(PenaltyBase):
    id: str
    type.name: Optional[str]
    type.nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

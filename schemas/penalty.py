import uuid

from typing import Optional, List


from schemas import NamedModel, ReadNamedModel
from schemas.base import CustomBaseModel


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

class PenaltyTypePaginationRead(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[PenaltyTypeRead]]

class PenaltyBase(CustomBaseModel):
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


class PenaltyPaginationRead(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[PenaltyRead]]


class PenaltyReadForOption(PenaltyBase):
    id: str
    type.name: Optional[str]
    type.nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

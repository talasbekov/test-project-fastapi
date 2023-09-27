import uuid

from typing import Optional, List
from pydantic import BaseModel

from schemas import NamedModel, ReadNamedModel


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

class PenaltyTypePaginationRead(BaseModel):
    total: Optional[int]
    objects: Optional[List[PenaltyTypeRead]]

class PenaltyBase(BaseModel):
    user_id: str
    type_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PenaltyCreate(PenaltyBase):
    pass


class PenaltyUpdate(PenaltyBase):
    pass


class PenaltyRead(PenaltyBase):
    id: str
    type: Optional[PenaltyTypeRead]

class PenaltyReadForOption(PenaltyBase):
    id: str
    type.name: Optional[str]
    type.nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

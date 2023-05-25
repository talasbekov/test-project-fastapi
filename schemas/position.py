import uuid
from typing import Optional

from schemas import Model, NamedModel, ReadModel, ReadNamedModel
from schemas import RankRead


class PositionBase(NamedModel):
    category_code: str


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionRead(PositionBase, ReadNamedModel):
    category_code: Optional[str]
    rank: Optional[RankRead]

    class Config:
        orm_mode = True

import uuid
from typing import Optional, Literal

from models.position import CategoryCodeEnum
from schemas import Model, NamedModel, ReadModel, ReadNamedModel
from schemas import RankRead


class PositionBase(NamedModel):
    category_code: str
    max_rank_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionRead(PositionBase, ReadNamedModel):
    category_code: Optional[str]

    max_rank_id: Optional[uuid.UUID]
    max_rank: Optional[RankRead]

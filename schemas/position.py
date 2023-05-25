import uuid
from typing import Optional

from schemas import Model, NamedModel, ReadModel, ReadNamedModel
from schemas import RankRead


class PositionBase(NamedModel):
    category_code: str
    max_rank_id: uuid.UUID


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionRead(PositionBase, ReadNamedModel):
    category_code: Optional[str]
    max_rank: Optional[RankRead]
    rank: Optional[RankRead]

    class Config:
        orm_mode = True

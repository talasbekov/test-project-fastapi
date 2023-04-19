import uuid
from typing import Optional

from schemas import Model, NamedModel, ReadModel, ReadNamedModel
from schemas import RankRead


class PositionBase(NamedModel):

    max_rank_id: uuid.UUID


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionRead(PositionBase, ReadNamedModel):

    max_rank_id: Optional[uuid.UUID]
    rank: Optional[RankRead]

    class Config:
        orm_mode = True

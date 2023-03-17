import uuid
from typing import Optional

from pydantic import BaseModel

from schemas import RankRead


class PositionBase(BaseModel):

    name: str
    max_rank_id: uuid.UUID


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionRead(PositionBase):

    id: Optional[uuid.UUID]
    name: Optional[str]
    max_rank_id: Optional[uuid.UUID]
    rank: Optional[RankRead]

    class Config:
        orm_mode = True

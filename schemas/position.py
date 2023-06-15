import uuid
from typing import Optional

from schemas import NamedModel, ReadNamedModel
from schemas import RankRead


class PositionBase(NamedModel):
    category_code: str
    form: str
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
    form: Optional[str]

    max_rank_id: Optional[uuid.UUID]
    max_rank: Optional[RankRead]

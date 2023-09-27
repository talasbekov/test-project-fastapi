import uuid
from typing import Optional, List

from schemas import NamedModel, ReadNamedModel, BaseModel, RankRead


class PositionBase(NamedModel):
    category_code: str
    form: str
    max_rank_id: Optional[str]

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

    max_rank_id: Optional[str]
    max_rank: Optional[RankRead]
    
class PositionPaginationRead(BaseModel):
    total: Optional[int]
    objects: Optional[List[PositionRead]]

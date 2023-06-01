import uuid
from typing import Optional

from models.position import CategoryCodeEnum
from schemas import NamedModel, ReadNamedModel
from schemas import RankRead


class ArchivePositionBase(NamedModel):
    category_code: CategoryCodeEnum
    max_rank_id: Optional[uuid.UUID]

class ArchivePositionAutoCreate(ArchivePositionBase):
    origin_id: uuid.UUID

class ArchivePositionCreate(ArchivePositionBase):
    pass


class ArchivePositionUpdate(ArchivePositionBase):
    pass


class ArchivePositionRead(ArchivePositionBase, ReadNamedModel):
    category_code: CategoryCodeEnum
    max_rank: Optional[RankRead]

    class Config:
        orm_mode = True

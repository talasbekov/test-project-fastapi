import uuid
from typing import Optional

from schemas import NamedModel, ReadNamedModel
from schemas import RankRead


class ArchivePositionBase(NamedModel):
    category_code: Optional[str]
    max_rank_id: Optional[uuid.UUID]

class ArchivePositionAutoCreate(ArchivePositionBase):
    origin_id: uuid.UUID

class ArchivePositionCreate(ArchivePositionBase):
    pass


class ArchivePositionUpdate(ArchivePositionBase):
    pass


class ArchivePositionRead(ArchivePositionBase, ReadNamedModel):
    max_rank: Optional[RankRead]

    class Config:
        orm_mode = True

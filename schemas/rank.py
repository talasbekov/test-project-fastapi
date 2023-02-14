import uuid

from pydantic import BaseModel
from typing import Optional


class RankBase(BaseModel):
    name: str


class RankCreate(RankBase):
    pass


class RankUpdate(RankBase):
    pass


class RankRead(RankBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True

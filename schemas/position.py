import uuid

from typing import Optional
from pydantic import BaseModel


class PositionBase(BaseModel):
    name: str
    max_rank_id: uuid.UUID
    description: Optional[str]


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionRead(PositionBase):
    id: uuid.UUID
    name: Optional[str]

    class Config:
        orm_mode = True

import uuid

from pydantic import BaseModel


class PositionBase(BaseModel):
    name: str
    max_rank_id: uuid.UUID
    description: str


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionRead(PositionBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

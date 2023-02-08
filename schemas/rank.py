import uuid

from pydantic import BaseModel


class RankBase(BaseModel):
    name: str
    url: str


class RankCreate(RankBase):
    pass


class RankUpdate(RankBase):
    pass


class RankRead(RankBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

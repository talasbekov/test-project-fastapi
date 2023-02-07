import uuid

from pydantic import BaseModel


class RankBase(BaseModel):
    name: str


class RankCreate(RankBase):
    url: str


class Rank(RankBase):
    id: str

    class Config:
        orm_mode = True
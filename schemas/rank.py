import uuid
from typing import Optional

from pydantic import BaseModel, AnyUrl


class RankBase(BaseModel):
    name: str


class RankCreate(RankBase):
    pass


class RankUpdate(RankBase):
    pass


class RankRead(RankBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    military_url: Optional[str]
    employee_url: Optional[str]

    class Config:
        orm_mode = True

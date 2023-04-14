import uuid
from typing import Optional

from pydantic import AnyUrl

from schemas import Model, NamedModel, ReadModel, ReadNamedModel



class RankBase(NamedModel):
    order: int
    military_url: AnyUrl
    employee_url: AnyUrl


class RankCreate(RankBase):
    pass


class RankUpdate(RankBase):
    pass


class RankRead(RankBase, ReadNamedModel):
    order: Optional[int]
    military_url: Optional[str]
    employee_url: Optional[str]

    class Config:
        orm_mode = True

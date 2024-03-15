from typing import Optional, List

from pydantic import AnyUrl, validator

from schemas import NamedModel, ReadNamedModel, BaseModel


class RankBase(NamedModel):
    rank_order: int
    military_url: AnyUrl
    employee_url: AnyUrl


class RankCreate(RankBase):
    military_url: Optional[AnyUrl]
    employee_url: Optional[AnyUrl]
    pass


class RankUpdate(RankBase):
    name: Optional[str]
    nameKZ: Optional[str]
    rank_order: Optional[int]
    military_url: Optional[AnyUrl]
    employee_url: Optional[AnyUrl]
    pass


class RankRead(RankBase, ReadNamedModel):
    
    rank_order: Optional[int]
    military_url: Optional[str]
    employee_url: Optional[str]
    
    class Config:
        orm_mode = True

class RankPaginationRead(BaseModel):
    total: Optional[int]
    objects: Optional[List[RankRead]]
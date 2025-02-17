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
    


class RankUpdate(RankBase):
    name: Optional[str]
    nameKZ: Optional[str]
    rank_order: Optional[int]
    military_url: Optional[AnyUrl]
    employee_url: Optional[AnyUrl]
    


class RankRead(RankBase, ReadNamedModel):
    
    rank_order: Optional[int]
    military_url: Optional[str] = None
    employee_url: Optional[str] = None

    @validator("military_url", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else " "
    
    class Config:
        orm_mode = True

class RankPaginationRead(BaseModel):
    total: Optional[int]
    objects: Optional[List[RankRead]]
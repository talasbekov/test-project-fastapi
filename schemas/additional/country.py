from typing import Optional, List

from schemas import NamedModel, ReadNamedModel, BaseModel


class CountryBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    pass


class CountryRead(CountryBase, ReadNamedModel):
    pass


class CountryReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[CountryRead]]

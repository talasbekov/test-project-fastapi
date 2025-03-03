from typing import Optional, List

from pydantic import BaseModel
from schemas import NamedModel, ReadNamedModel, CustomBaseModel


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


class CountryReadPagination(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[CountryRead]]

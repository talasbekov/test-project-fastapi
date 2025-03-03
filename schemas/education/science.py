from typing import Optional, List
from pydantic import BaseModel
from schemas import NamedModel, ReadNamedModel, CustomBaseModel


class ScienceBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ScienceCreate(ScienceBase):
    pass


class ScienceUpdate(ScienceBase):
    pass


class ScienceRead(ScienceBase, ReadNamedModel):
    pass


class ScienceReadPagination(CustomBaseModel):
    total: Optional[int]
    objects: Optional[List[ScienceRead]]

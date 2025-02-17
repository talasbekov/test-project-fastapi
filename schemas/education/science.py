from typing import Optional, List

from schemas import NamedModel, ReadNamedModel, BaseModel


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


class ScienceReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[ScienceRead]]

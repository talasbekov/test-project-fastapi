from schemas import NamedModel, ReadNamedModel, BaseModel
from typing import Optional, List


class SportDegreeTypeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SportDegreeTypeCreate(SportDegreeTypeBase):
    pass


class SportDegreeTypeUpdate(SportDegreeTypeBase):
    pass


class SportDegreeTypeRead(SportDegreeTypeBase, ReadNamedModel):
    pass

class SportDegreeTypePaginationRead(BaseModel):
    total: Optional[int]
    objects: Optional[List[SportDegreeTypeRead]]

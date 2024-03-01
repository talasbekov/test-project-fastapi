from schemas import NamedModel, ReadNamedModel, BaseModel
from typing import Optional, List


class PropertyTypeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PropertyTypeCreate(PropertyTypeBase):
    pass


class PropertyTypeUpdate(PropertyTypeBase):
    pass


class PropertyTypeRead(PropertyTypeBase, ReadNamedModel):
    pass

class PropertyTypePaginationRead(BaseModel):
    total: Optional[int]
    objects: Optional[List[PropertyTypeRead]]

from schemas import NamedModel, ReadNamedModel, Model
from typing import Optional, List
from pydantic import BaseModel


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

class PropertyTypePaginationRead(Model):
    total: Optional[int]
    objects: Optional[List[PropertyTypeRead]]

import uuid
from typing import Optional

from pydantic import BaseModel
from schemas import Model, NamedModel, ReadModel, ReadNamedModel


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

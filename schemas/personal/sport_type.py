import uuid
from typing import Optional

from pydantic import BaseModel
from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class SportTypeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SportTypeCreate(SportTypeBase):
    pass


class SportTypeUpdate(SportTypeBase):
    pass


class SportTypeRead(SportTypeBase, ReadNamedModel):
    pass

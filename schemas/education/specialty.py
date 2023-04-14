import uuid
from typing import Optional

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class SpecialtyBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SpecialtyCreate(SpecialtyBase):
    pass


class SpecialtyUpdate(SpecialtyBase):
    pass


class SpecialtyRead(SpecialtyBase, ReadNamedModel):
    pass

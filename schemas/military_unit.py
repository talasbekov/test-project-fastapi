import uuid
from typing import Optional

from pydantic import BaseModel
from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class MilitaryUnitBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class MilitaryUnitCreate(MilitaryUnitBase):
    pass


class MilitaryUnitUpdate(MilitaryUnitBase):
    pass


class MilitaryUnitRead(MilitaryUnitBase, ReadNamedModel):
    pass

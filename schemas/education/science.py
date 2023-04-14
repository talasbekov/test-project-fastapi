import uuid
from typing import Optional

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


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

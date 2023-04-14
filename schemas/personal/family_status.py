import uuid
from typing import Optional

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class FamilyStatusBase(NamedModel):
    pass


class FamilyStatusCreate(FamilyStatusBase):
    pass


class FamilyStatusUpdate(FamilyStatusBase):
    pass


class FamilyStatusRead(FamilyStatusBase, ReadNamedModel):

    class Config:
        orm_mode = True

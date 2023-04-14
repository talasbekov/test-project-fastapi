import uuid
from typing import Optional

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class JurisdictionBase(NamedModel):
    pass


class JurisdictionCreate(JurisdictionBase):
    pass


class JurisdictionUpdate(JurisdictionBase):
    pass


class JurisdictionRead(JurisdictionBase, ReadNamedModel):

    class Config:
        orm_mode = True

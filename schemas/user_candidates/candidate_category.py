import uuid
import datetime
from typing import Optional

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class CandidateCategoryBase(NamedModel):
    pass


class CandidateCategoryCreate(CandidateCategoryBase):
    pass


class CandidateCategoryUpdate(CandidateCategoryBase):
    pass


class CandidateCategoryRead(CandidateCategoryBase, ReadNamedModel):

    class Config:
        orm_mode = True

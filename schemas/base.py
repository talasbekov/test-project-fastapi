import uuid
import datetime
from typing import Optional

from pydantic import BaseModel


class Model(BaseModel):

    class Config:
        orm_mode = True


class NamedModel(Model):
    name: str
    nameKZ: Optional[str]

    class Config:
        orm_mode = True


class ReadModel(Model):
    id: Optional[uuid.UUID]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class ReadNamedModel(NamedModel, ReadModel):
    name: Optional[str]
    nameKZ: Optional[str]

    class Config:
        orm_mode = True

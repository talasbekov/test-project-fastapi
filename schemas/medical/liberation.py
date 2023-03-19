import uuid
from typing import Optional

from pydantic import BaseModel


class LiberationBase(BaseModel):
    name: str


class LiberationCreate(LiberationBase):
    pass


class LiberationUpdate(LiberationBase):
    pass


class LiberationRead(LiberationBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True

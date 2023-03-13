import uuid

from typing import Optional

from pydantic import BaseModel


class AgeGroupBase(BaseModel):
    group: int


class AgeGroupCreate(AgeGroupBase):
    pass


class AgeGroupUpdate(AgeGroupBase):
    pass


class AgeGroupRead(AgeGroupBase):
    id: Optional[uuid.UUID]
    group: Optional[int]

    class Config:
        orm_mode = True

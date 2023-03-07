import uuid

from pydantic import BaseModel
from typing import Optional


class ProfileBase(BaseModel):
    pass


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: Optional[uuid.UUID]

    class Config:
        orm_mode = True

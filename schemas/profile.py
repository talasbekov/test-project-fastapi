import uuid
from typing import Optional

from pydantic import BaseModel


class ProfileBase(BaseModel):
    user_id: uuid.UUID


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StatusBase(BaseModel):
    name: str
    user_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StatusCreate(StatusBase):
    pass


class StatusUpdate(StatusBase):
    pass


class StatusRead(StatusBase):
    id: uuid.UUID

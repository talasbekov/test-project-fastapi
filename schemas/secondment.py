import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SecondmentBase(BaseModel):
    name: Optional[str]
    user_id: uuid.UUID
    staff_division_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SecondmentCreate(SecondmentBase):
    pass


class SecondmentUpdate(SecondmentBase):
    pass


class SecondmentRead(SecondmentBase):
    id: uuid.UUID

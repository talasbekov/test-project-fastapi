import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StatusTypeBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        
class StatusTypeCreate(StatusTypeBase):
    pass


class StatusTypeUpdate(StatusTypeBase):
    pass


class StatusTypeRead(StatusTypeBase):
    id: uuid.UUID
    name: str


class StatusBase(BaseModel):
    type_id: uuid.UUID
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
    
    type: Optional[StatusTypeRead]

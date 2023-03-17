import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EventBase(BaseModel):
    user_id: uuid.UUID
    name: str
    date_since: datetime
    date_to: datetime


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventRead(EventBase):
    id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    name: Optional[str]
    date_since: Optional[datetime]
    date_to: Optional[datetime]

    class Config:
        orm_mode = True

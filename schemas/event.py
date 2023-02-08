import uuid
from datetime import datetime

from pydantic import BaseModel
from typing import List, Dict, Any


class EventBase(BaseModel):
    user_id: str
    name: str
    date_since: datetime
    date_to: datetime


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventRead(EventBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

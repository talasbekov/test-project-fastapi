import uuid
from datetime import datetime
from typing import Optional

from schemas import NamedModel, ReadNamedModel


class EventBase(NamedModel):
    user_id: str
    date_since: datetime
    date_to: datetime


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventRead(EventBase, ReadNamedModel):
    user_id: Optional[str]
    date_since: Optional[datetime]
    date_to: Optional[datetime]

    class Config:
        orm_mode = True

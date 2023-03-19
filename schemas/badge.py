import uuid
from typing import Optional

from pydantic import BaseModel


class BadgeBase(BaseModel):
    name: str
    url: str


class BadgeCreate(BadgeBase):
    pass


class BadgeUpdate(BadgeBase):
    pass


class BadgeRead(BadgeBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    url: Optional[str]

    class Config:
        orm_mode = True

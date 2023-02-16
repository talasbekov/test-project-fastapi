import uuid

from pydantic import BaseModel
from typing import Optional


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

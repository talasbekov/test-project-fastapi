import uuid

from pydantic import BaseModel


class BadgeBase(BaseModel):
    name: str


class BadgeCreate(BadgeBase):
    url: str


class Badge(BadgeBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
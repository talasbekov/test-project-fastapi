import uuid

from pydantic import BaseModel


class BadgeBase(BaseModel):
    name: str


class BadgeCreate(BadgeBase):
    url: str


class Badge(BadgeBase):
    id: str

    class Config:
        orm_mode = True
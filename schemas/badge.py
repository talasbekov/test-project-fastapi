import uuid

from pydantic import BaseModel


class BadgeBase(BaseModel):
    name: str
    url: str


class BadgeCreate(BadgeBase):
    pass


class BadgeUpdate(BadgeBase):
    pass


class BadgeRead(BadgeBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

import uuid
from typing import Optional

from pydantic import BaseModel


class BadgeTypeBase(BaseModel):
    name: str
    url: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BadgeTypeCreate(BadgeTypeBase):
    pass


class BadgeTypeUpdate(BadgeTypeBase):
    pass


class BadgeTypeRead(BadgeTypeBase):
    id: uuid.UUID
    name: str
    url: str


class BadgeBase(BaseModel):
    user_id: uuid.UUID
    type_id: uuid.UUID


class BadgeCreate(BadgeBase):
    pass


class BadgeUpdate(BadgeBase):
    pass


class BadgeRead(BadgeBase):
    id: Optional[uuid.UUID]
    type: Optional[BadgeTypeRead]

    class Config:
        orm_mode = True

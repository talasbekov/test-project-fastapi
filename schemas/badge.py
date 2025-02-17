import uuid
from typing import Optional, List
from datetime import datetime

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class BadgeTypeBase(NamedModel):
    url: Optional[str]
    badge_order: Optional[int]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BadgeTypeCreate(BadgeTypeBase):
    pass


class BadgeTypeUpdate(BadgeTypeBase):
    pass


class BadgeTypeRead(BadgeTypeBase, ReadNamedModel):
    url: Optional[str]

class BadgeTypePaginationRead(Model):
    total: Optional[int]
    objects: Optional[List[BadgeTypeRead]]

class BadgeBase(Model):
    user_id: str
    type_id: Optional[str]


class BadgeCreate(BadgeBase):
    pass


class BadgeUpdate(BadgeBase):
    pass


class History(Model):
    date_from: Optional[datetime]
    date_to: Optional[datetime]


class BadgeRead(BadgeBase, ReadModel):
    type: Optional[BadgeTypeRead]
    history: Optional[History]

    class Config:
        orm_mode = True

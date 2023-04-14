import uuid
from typing import Optional

from schemas import Model, NamedModel, ReadModel, ReadNamedModel

class BadgeTypeBase(NamedModel):
    url: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BadgeTypeCreate(BadgeTypeBase):
    pass


class BadgeTypeUpdate(BadgeTypeBase):
    pass


class BadgeTypeRead(BadgeTypeBase, ReadNamedModel):
    url: str


class BadgeBase(Model):
    user_id: uuid.UUID
    type_id: uuid.UUID


class BadgeCreate(BadgeBase):
    pass


class BadgeUpdate(BadgeBase):
    pass


class BadgeRead(BadgeBase, ReadModel):
    type: Optional[BadgeTypeRead]

    class Config:
        orm_mode = True

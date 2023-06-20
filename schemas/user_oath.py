import uuid
from datetime import datetime
from typing import Optional


from schemas import MilitaryUnitRead
from schemas import Model, ReadModel


class UserOath(Model):
    date: Optional[datetime]
    user_id: uuid.UUID
    military_unit_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserOathCreate(UserOath):
    pass


class UserOathUpdate(UserOath):
    pass


class UserOathRead(UserOath, ReadModel):
    military_unit: Optional[MilitaryUnitRead]

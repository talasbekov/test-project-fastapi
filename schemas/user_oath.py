import uuid
from datetime import date
from typing import Optional


from schemas import MilitaryUnitRead
from schemas import Model, ReadModel


class UserOath(Model):
    date: Optional[date]
    user_id: str
    military_unit: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserOathCreate(UserOath):
    pass


class UserOathUpdate(UserOath):
    pass


class UserOathRead(UserOath, ReadModel):
    military_unit: Optional[str]

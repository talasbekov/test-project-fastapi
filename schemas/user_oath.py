import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from schemas import MilitaryUnitRead


class UserOath(BaseModel):
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


class UserOathRead(UserOath):
    id: uuid.UUID
    military_unit = Optional[MilitaryUnitRead]

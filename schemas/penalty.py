import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PenaltyTypeBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PenaltyTypeCreate(PenaltyTypeBase):
    pass


class PenaltyTypeUpdate(PenaltyTypeBase):
    pass


class PenaltyTypeRead(PenaltyTypeBase):
    name: str


class PenaltyBase(BaseModel):
    user_id: uuid.UUID
    type_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PenaltyCreate(PenaltyBase):
    pass


class PenaltyUpdate(PenaltyBase):
    pass


class PenaltyRead(PenaltyBase):
    id: uuid.UUID

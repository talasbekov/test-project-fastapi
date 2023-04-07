import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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

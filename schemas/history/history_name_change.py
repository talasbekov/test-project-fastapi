import uuid
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class HistoryNameChangeBase(Model):
    name_before: Optional[str]
    name_after: Optional[str]
    user_id: uuid.UUID
    name_type: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class HistoryNameChangeCreate(HistoryNameChangeBase):
    pass


class HistoryNameChangeUpdate(HistoryNameChangeBase):
    pass


class HistoryNameChangeRead(HistoryNameChangeBase, ReadModel):
    name_before: Optional[str]
    name_after: Optional[str]
    user_id: Optional[uuid.UUID]
    name_type: Optional[str]

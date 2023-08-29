import uuid
from typing import Optional

from schemas import Model, ReadModel


class HistoryNameChangeBase(Model):
    name_before: Optional[str]
    name_after: Optional[str]
    user_id: str
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
    user_id: Optional[str]
    name_type: Optional[str]

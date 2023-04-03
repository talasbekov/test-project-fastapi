from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class History(BaseModel):
    date_from: Optional[str]
    date_to: Optional[str]
    user_id: Optional[UUID]
    type: str
    staff_unit_id: Optional[UUID]
    rank_id: Optional[UUID]
    position_id: Optional[UUID]
    equipment_id: Optional[UUID]


    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class HistoryCreate(History):
    pass


class HistoryUpdate(History):
    pass


class HistoryRead(History):
    id: Optional[UUID]

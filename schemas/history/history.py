from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class HistoryBase(BaseModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    staff_unit_id: Optional[uuid.UUID]
    rank_id: Optional[uuid.UUID]
    position_id: Optional[uuid.UUID]
    equipment_id: Optional[uuid.UUID]
    name: Optional[str]
    user_id: uuid.UUID
    type: str
    

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class HistoryCreate(HistoryBase):
    pass


class HistoryUpdate(HistoryBase):
    pass


class HistoryRead(HistoryBase):
    id: uuid.UUID

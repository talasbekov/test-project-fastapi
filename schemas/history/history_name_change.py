from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class HistoryNameChangeBase(BaseModel):
    name_before: Optional[str]
    name_after: Optional[str]
    name_type: str
    
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class HistoryNameChangeCreate(HistoryNameChangeBase):
    pass


class HistoryNameChangeUpdate(HistoryNameChangeBase):
    pass


class HistoryNameChangeRead(HistoryNameChangeBase):
    id: uuid.UUID

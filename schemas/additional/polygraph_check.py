from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class PolygraphCheckBase(BaseModel):
    number: str
    issued_by: str
    date_of_issue: datetime
    document_link: str
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PolygraphCheckCreate(PolygraphCheckBase):
    profile_id: Optional[uuid.UUID]
    


class PolygraphCheckUpdate(PolygraphCheckBase):
    pass

class PolygraphCheckRead(PolygraphCheckBase):
    profile_id: uuid.UUID
    id: uuid.UUID

from pydantic import BaseModel
from datetime import datetime
import uuid

class PolygraphCheckBase(BaseModel):
    number: str
    issued_by: str
    date_of_issue: datetime
    document_link: str
    profile_id: uuid.UUID
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PolygraphCheckCreate(PolygraphCheckBase):
    pass


class PolygraphCheckUpdate(PolygraphCheckBase):
    pass

class PolygraphCheckRead(PolygraphCheckBase):
    id: uuid.UUID


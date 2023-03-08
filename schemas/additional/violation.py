from pydantic import BaseModel
from datetime import datetime
import uuid


class ViolationBase(BaseModel):
    name: str
    date: datetime
    issued_by: str
    article_number: str
    consequence: str
    profile_id: uuid.UUID
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ViolationCreate(ViolationBase):
    pass


class ViolationUpdate(ViolationBase):
    pass


class ViolationRead(ViolationBase):
    id: uuid.UUID    

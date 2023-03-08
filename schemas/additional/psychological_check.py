from pydantic import BaseModel
from datetime import datetime
import uuid


class PsychologicalCheckBase(BaseModel):
    issued_by: str
    date_of_issue: datetime
    document_link: str
    profile_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class PsychologicalCheckCreate(PsychologicalCheckBase):
    pass

class PsychologicalCheckUpdate(PsychologicalCheckBase):
    pass

class PsychologicalCheckRead(PsychologicalCheckBase):
    id: uuid.UUID
    

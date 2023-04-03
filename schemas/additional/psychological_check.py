import uuid
from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel


class PsychologicalCheckBase(BaseModel):
    issued_by: str
    date_of_issue: datetime
    document_link: AnyUrl
    profile_id: uuid.UUID
    document_number: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class PsychologicalCheckCreate(PsychologicalCheckBase):
    pass

class PsychologicalCheckUpdate(PsychologicalCheckBase):
    pass

class PsychologicalCheckRead(PsychologicalCheckBase):
    id: uuid.UUID
    
    document_link: Optional[str]

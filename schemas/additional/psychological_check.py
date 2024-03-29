import uuid
from datetime import datetime
from typing import Optional

from pydantic import AnyUrl
from schemas import Model, ReadModel


class PsychologicalCheckBase(Model):
    issued_by: str
    date_of_issue: datetime
    document_link: Optional[AnyUrl]
    profile_id: str
    document_number: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PsychologicalCheckCreate(PsychologicalCheckBase):
    pass


class PsychologicalCheckUpdate(PsychologicalCheckBase):
    pass


class PsychologicalCheckRead(PsychologicalCheckBase, ReadModel):
    document_link: Optional[str]

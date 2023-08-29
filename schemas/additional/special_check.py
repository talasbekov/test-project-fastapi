import uuid
from datetime import datetime
from typing import Optional

from pydantic import AnyUrl
from schemas import Model, ReadModel


class SpecialCheckBase(Model):
    number: str
    issued_by: str
    date_of_issue: datetime
    document_link: Optional[AnyUrl]
    profile_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SpecialCheckCreate(SpecialCheckBase):
    pass


class SpecialCheckUpdate(SpecialCheckBase):
    id: str


class SpecialCheckRead(SpecialCheckBase, ReadModel):
    document_link: Optional[str]

import uuid
from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel
from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class SpecialCheckBase(Model):
    number: str
    issued_by: str
    date_of_issue: datetime
    document_link: AnyUrl
    profile_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SpecialCheckCreate(SpecialCheckBase):
    pass

class SpecialCheckUpdate(SpecialCheckBase):
    id: uuid.UUID


class SpecialCheckRead(SpecialCheckBase, ReadModel):
    document_link: Optional[str]

from pydantic import BaseModel
import datetime
import uuid

class SpecialCheckBase(BaseModel):
    number: str
    issued_by: str
    date_of_issue: datetime
    document_link: str
    profile_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SpecialCheckCreate(SpecialCheckBase):
    pass

class SpecialCheckUpdate(SpecialCheckBase):
    id: uuid.UUID


class SpecialCheckRead(SpecialCheckBase):
    id: uuid.UUID

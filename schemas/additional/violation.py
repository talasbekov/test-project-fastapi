import uuid
from datetime import datetime
from typing import Optional

from pydantic import AnyUrl

from schemas import NamedModel, ReadNamedModel


class ViolationBase(NamedModel):
    date: datetime
    issued_by: str
    article_number: str
    consequence: str
    document_link: Optional[AnyUrl]
    profile_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ViolationCreate(ViolationBase):
    pass


class ViolationUpdate(ViolationBase):
    pass


class ViolationRead(ViolationBase, ReadNamedModel):
    pass

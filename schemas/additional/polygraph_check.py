import uuid
from datetime import datetime
from typing import Optional

from pydantic import AnyUrl

from schemas import Model, ReadModel


class PolygraphCheckBase(Model):
    number: str
    issued_by: str
    date_of_issue: datetime
    document_link: Optional[AnyUrl]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PolygraphCheckCreate(PolygraphCheckBase):
    profile_id: Optional[str]


class PolygraphCheckUpdate(PolygraphCheckBase):
    pass


class PolygraphCheckRead(PolygraphCheckBase, ReadModel):
    profile_id: str
    document_link: Optional[str]

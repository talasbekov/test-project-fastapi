import uuid
from datetime import datetime
from typing import Optional

from pydantic import constr, BaseModel

from schemas import NamedModel, ReadNamedModel, Model
from .violation_type import ViolationTypeRead


class ViolationBase(Model):
    date: datetime
    issued_by: str
    issued_byKZ: str
    article_number: str
    article_numberKZ: str
    consequence: str
    consequenceKZ: str
    document_link: Optional[constr(min_length=0)] = None
    profile_id: Optional[str]
    violation_type_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ViolationCreate(ViolationBase):
    pass


class ViolationUpdate(ViolationBase):
    pass


class ViolationRead(ViolationBase, ReadNamedModel):
    issued_byKZ: Optional[str]
    article_numberKZ: Optional[str]
    consequenceKZ: Optional[str]
    violation_type: Optional[ViolationTypeRead]

import uuid
from datetime import datetime
from typing import Optional, List

from schemas import Model, NamedModel, ReadModel, ReadNamedModel, BaseModel


class StatusTypeBase(NamedModel):
    pass


class StatusTypeCreate(StatusTypeBase):
    pass


class StatusTypeUpdate(StatusTypeBase):
    pass


class StatusTypeRead(StatusTypeBase, ReadNamedModel):
    pass

class StatusTypePaginationRead(BaseModel):
    total: Optional[int]
    objects: Optional[List[StatusTypeRead]]

class History(Model):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    status_name: Optional[str]


class StatusBase(Model):
    type_id: Optional[str]
    user_id: str


class StatusCreate(StatusBase):
    pass


class StatusUpdate(StatusBase):
    pass


class StatusRead(StatusBase, ReadModel):
    type: Optional[StatusTypeRead]
    history: Optional[History]

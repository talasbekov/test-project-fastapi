import uuid
from datetime import datetime
from typing import Optional

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class StatusTypeBase(NamedModel):
    pass


class StatusTypeCreate(StatusTypeBase):
    pass


class StatusTypeUpdate(StatusTypeBase):
    pass


class StatusTypeRead(StatusTypeBase, ReadNamedModel):
    pass


class History(Model):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    status_name: Optional[str]


class StatusBase(Model):
    type_id: uuid.UUID
    user_id: uuid.UUID


class StatusCreate(StatusBase):
    pass


class StatusUpdate(StatusBase):
    pass


class StatusRead(StatusBase, ReadModel):
    type: Optional[StatusTypeRead]
    history: Optional[History]

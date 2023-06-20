import uuid
from typing import Optional

from schemas import Model, ReadModel


class NotificationBase(Model):
    message: str
    sender_id: uuid.UUID
    receiver_id: uuid.UUID

    class Config():
        orm_mode = True
        arbitrary_types_allowed = True


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(NotificationBase):
    pass


class NotificationRead(ReadModel, NotificationBase):
    message: Optional[str]
    sender_id: Optional[uuid.UUID]
    receiver_id: Optional[uuid.UUID]

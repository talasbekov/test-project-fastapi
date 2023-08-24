import uuid
from typing import Optional

from schemas import Model, ReadModel


class NotificationBase(Model):
    message: str
    sender_id: str
    receiver_id: str

    class Config():
        orm_mode = True
        arbitrary_types_allowed = True


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(NotificationBase):
    pass


class NotificationRead(ReadModel, NotificationBase):
    message: Optional[str]
    sender_id: Optional[str]
    receiver_id: Optional[str]

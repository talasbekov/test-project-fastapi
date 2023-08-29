import uuid
from typing import Optional
from datetime import datetime

from models import ServiceIDStatus
from schemas import Model, ReadModel


class ServiceIDBase(Model):
    number: Optional[str]
    date_to: Optional[datetime]
    token_status: Optional[ServiceIDStatus]
    id_status: Optional[ServiceIDStatus]
    user_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ServiceIDCreate(ServiceIDBase):
    pass


class ServiceIDUpdate(ServiceIDBase):
    pass


class ServiceIDRead(ServiceIDBase, ReadModel):
    pass

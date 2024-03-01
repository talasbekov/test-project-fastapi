import uuid
from datetime import datetime, date
from typing import Optional

from models import ServiceIDStatus
from schemas import Model, ReadModel


class ServiceIDBase(Model):
    number: Optional[str]
    date_to: Optional[date]
    token_status: Optional[str]
    token_number: Optional[str]
    id_status: Optional[str]
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

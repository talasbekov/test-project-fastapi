import uuid
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from models import ServiceIDStatus
from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class ServiceIDBase(Model):
    number: Optional[str]
    date_to: Optional[datetime]
    token_status: Optional[ServiceIDStatus]
    id_status: Optional[ServiceIDStatus]
    user_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ServiceIDCreate(ServiceIDBase):
    pass


class ServiceIDUpdate(ServiceIDBase):
    pass


class ServiceIDRead(ServiceIDBase, ReadModel):
    pass

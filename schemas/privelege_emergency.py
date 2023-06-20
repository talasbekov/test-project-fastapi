import uuid
from typing import Optional

from datetime import datetime
from enum import Enum

from schemas import Model, ReadModel


class PrivelegeEmergency(Model):
    form: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    user_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PrivelegeEmergencyCreate(PrivelegeEmergency):
    pass


class PrivelegeEmergencyUpdate(PrivelegeEmergency):
    pass


class PrivelegeEmergencyRead(PrivelegeEmergency, ReadModel):
    form: Optional[Enum]
    pass

import uuid
from typing import Optional

from datetime import date
from enum import Enum

from schemas import Model, ReadModel


class PrivelegeEmergency(Model):
    form: Optional[str]
    date_from: Optional[date]
    date_to: Optional[date]
    user_id: Optional[str]

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

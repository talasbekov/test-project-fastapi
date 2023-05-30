import uuid
from typing import Optional

from datetime import datetime
from enum import Enum

from schemas import Model, ReadModel


class ArchivePrivelegeEmergency(Model):
    form: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    user_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ArchivePrivelegeEmergencyCreate(ArchivePrivelegeEmergency):
    pass


class ArchivePrivelegeEmergencyAutoCreate(ArchivePrivelegeEmergency):
    origin_id: Optional[uuid.UUID]
    pass


class ArchivePrivelegeEmergencyUpdate(ArchivePrivelegeEmergency):
    pass


class ArchivePrivelegeEmergencyRead(ArchivePrivelegeEmergency, ReadModel):
    form: Optional[Enum]
    pass

import uuid
from typing import Optional

from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class PersonnalReserveBase(Model):
    reserve: Optional[Enum]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    user_id: Optional[uuid.UUID]
    document_link: Optional[str]
    document_number: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
 

class PersonnalReserveCreate(PersonnalReserveBase):
    pass


class PersonnalReserveUpdate(PersonnalReserveBase):
    pass


class PersonnalReserveRead(PersonnalReserveBase, ReadModel):
    pass

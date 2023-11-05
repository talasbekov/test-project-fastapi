
from typing import Optional
from enum import Enum
from datetime import date

from schemas import Model, ReadModel


class PersonnalReserveBase(Model):
    reserve: Optional[str]
    reserve_date: Optional[date]
    user_id: Optional[str]
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
    reserve: Optional[Enum]

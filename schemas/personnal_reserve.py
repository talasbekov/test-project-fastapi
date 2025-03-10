import uuid
from typing import Optional
from enum import Enum
from datetime import date
from pydantic import root_validator

from models import ReserveEnum
from schemas import Model, ReadModel
from schemas.base import Model


class PersonnalReserveBase(ReadModel, Model):
    reserve: Optional[ReserveEnum]
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

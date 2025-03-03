import uuid
from typing import Optional
from enum import Enum
from datetime import date
from pydantic import root_validator

from models import ReserveEnum
from schemas import Model, ReadModel
from schemas.base import CustomBaseModel


class PersonnalReserveBase(ReadModel, CustomBaseModel):
    reserve: Optional[ReserveEnum]
    reserve_date: Optional[date]
    user_id: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def fill_none_values(cls, values):
        # Преобразуем GetterDict в обычный dict
        values = dict(values)

        """
        Если поле None, заменяем его "жёстким" значением:
         - reserve → "Данные отсутствуют!"
         - reserve_date → date(1920, 1, 1)
         - user_id → "missing_user"
         - document_link → "Данные отсутствуют!"
         - document_number → "Данные отсутствуют!"
        """
        values["reserve"] = values.get("reserve") or ReserveEnum.ENLISTED.value
        values["reserve_date"] = values.get("reserve_date") or date(1920, 1, 1)
        values["user_id"] = values.get("user_id") or str(uuid.uuid4())
        values["document_link"] = values.get("document_link") or "Данные отсутствуют!"
        values["document_number"] = values.get("document_number") or "Данные отсутствуют!"

        return values


class PersonnalReserveCreate(PersonnalReserveBase):
    pass


class PersonnalReserveUpdate(PersonnalReserveBase):
    pass


class PersonnalReserveRead(PersonnalReserveBase, ReadModel):
    reserve: Optional[Enum]

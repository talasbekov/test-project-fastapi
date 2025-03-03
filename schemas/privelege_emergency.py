import uuid

from pydantic import root_validator
from typing import Optional

from datetime import date
from enum import Enum

from models import FormEnum
from schemas import Model, ReadModel


class PrivelegeEmergency(Model):
    form: Optional[FormEnum]
    date_from: Optional[date]
    date_to: Optional[date]
    user_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def fill_none_values(cls, values):
        # Превращаем GetterDict в обычный dict, чтобы можно было делать item assignment
        values = dict(values)
        """
        Если какое-то поле None, заменяем его "хардкод" значением:
         - form: FormEnum.form2
         - date_from: date(1920,1,1)
         - date_to: date(2500,1,1)
         - user_id: "missing_user"
        """
        if values.get("form") is None:
            values["form"] = FormEnum.form2

        if values.get("date_from") is None:
            # Подставляем дату 1920-01-01
            values["date_from"] = date(1920, 1, 1)

        if values.get("date_to") is None:
            values["date_to"] = date(2500, 1, 1)

        if values.get("user_id") is None:
            values["user_id"] = str(uuid.uuid4())

        return values


class PrivelegeEmergencyCreate(PrivelegeEmergency):
    pass


class PrivelegeEmergencyUpdate(PrivelegeEmergency):
    pass


class PrivelegeEmergencyRead(PrivelegeEmergency, ReadModel):
    form: Optional[Enum]
    pass

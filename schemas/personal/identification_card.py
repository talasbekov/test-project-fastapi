import datetime
from datetime import date
from typing import Optional

from pydantic import AnyUrl, BaseModel, root_validator

from schemas import CustomBaseModel


class IdentificationCardBase(CustomBaseModel):
    document_number: str
    date_of_issue: datetime.date
    date_to: datetime.date
    issued_by: str
    document_link: Optional[AnyUrl]
    profile_id: str


class IdentificationCardCreate(IdentificationCardBase):
    pass


class IdentificationCardUpdate(CustomBaseModel):
    document_number: Optional[str]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    issued_by: Optional[str]
    document_link: Optional[AnyUrl]


class IdentificationCardRead(IdentificationCardBase):
    id: str
    document_number: Optional[str] = "Данные отсутствуют!"
    date_of_issue: Optional[date] = date(1920, 1, 1)
    date_to: Optional[date] = date(2500, 1, 1)
    issued_by: Optional[str] = "Данные отсутствуют!"
    document_link: Optional[str] = "Данные отсутствуют!"
    profile_id: str
    created_at: Optional[date] = date(1920, 1, 1)
    updated_at: Optional[date] = date(1920, 1, 1)

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def fill_none_values(cls, values):
        # Преобразуем GetterDict в dict
        values = dict(values)

        defaults = {
            "document_number": "Данные отсутствуют!",
            "date_of_issue": date(1920, 1, 1),
            "date_to": date(2500, 1, 1),
            "issued_by": "Данные отсутствуют!",
            "document_link": "Данные отсутствуют!",
            "created_at": date(1920, 1, 1),
            "updated_at": date(1920, 1, 1),
        }

        for key, default in defaults.items():
            values[key] = values.get(key) or default

        return values

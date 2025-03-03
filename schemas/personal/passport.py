import datetime
from datetime import date
from typing import Optional

from pydantic import BaseModel, validator, root_validator, AnyUrl

from schemas import CustomBaseModel


class PassportBase(CustomBaseModel):
    document_number: str
    date_of_issue: datetime.date
    date_to: datetime.date
    document_link: Optional[AnyUrl]
    profile_id: str
    issued_by: str


class PassportCreate(PassportBase):
    pass


class PassportUpdate(CustomBaseModel):
    document_number: Optional[str]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    document_link: Optional[AnyUrl]
    profile_id: Optional[str]
    issued_by: Optional[str]


class PassportRead(PassportBase):
    id: str
    document_number: Optional[str] = "Данные отсутствуют!"
    date_of_issue: Optional[date] = date(1920, 1, 1)
    date_to: Optional[date] = date(2500, 1, 1)
    document_link: Optional[str] = "https://10.15.3.180/s3/static/placeholder.jpg"
    issued_by: Optional[str] = "Данные отсутствуют!"
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
            "document_link": "https://10.15.3.180/s3/static/placeholder.jpg",
            "created_at": date(1920, 1, 1),
            "updated_at": date(1920, 1, 1),
        }

        for key, default in defaults.items():
            values[key] = values.get(key) or default

        return values

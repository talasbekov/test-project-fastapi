import datetime
from datetime import date
from typing import List, Optional, Union

from pydantic import BaseModel, AnyUrl, root_validator

from schemas import CustomBaseModel


class DrivingLicenseLinkUpdate(CustomBaseModel):
    document_link: Optional[AnyUrl]


class DrivingLicenseBase(CustomBaseModel):
    document_number: str
    category: List[str]
    date_of_issue: datetime.date
    date_to: datetime.date
    document_link: Optional[AnyUrl]
    profile_id: str


class DrivingLicenseCreate(DrivingLicenseBase):
    category: Optional[str]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]


class DrivingLicenseUpdate(CustomBaseModel):
    document_number: Optional[str]
    category: Optional[str]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    document_link: Optional[AnyUrl]
    # profile_id: str


class DrivingLicenseRead(DrivingLicenseBase):
    id: str
    document_number: Optional[str] = "Данные отсутствуют!"
    category: Union[Optional[str], Optional[List[str]]] = "Данные отсутствуют!"
    date_of_issue: Optional[date] = date(1920, 1, 1)
    date_to: Optional[date] = date(2500, 1, 1)
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
            "category": "Данные отсутствуют!",
            "date_of_issue": date(1920, 1, 1),
            "date_to": date(2500, 1, 1),
            "document_link": "Данные отсутствуют!",
            "created_at": date(1920, 1, 1),
            "updated_at": date(1920, 1, 1),
        }

        for key, default in defaults.items():
            values[key] = values.get(key) or default

        return values

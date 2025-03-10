import datetime
from typing import Optional

from schemas import Model


class UserFinancialInfoBase(Model):
    iban: str
    housing_payments_iban: str
    profile_id: str


class UserFinancialInfoCreate(UserFinancialInfoBase):
    pass


class UserFinancialInfoUpdate(UserFinancialInfoBase):
    pass


class UserFinancialInfoRead(UserFinancialInfoBase):
    id: Optional[str]
    iban: Optional[str]
    housing_payments_iban: Optional[str]
    profile_id: Optional[str]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True

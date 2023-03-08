import uuid
import datetime

from typing import Optional, List

from pydantic import BaseModel


class UserFinancialInfoBase(BaseModel):
    iban: str
    housing_payments_iban: str
    profile_id: uuid.UUID


class UserFinancialInfoCreate(UserFinancialInfoBase):
    pass


class UserFinancialInfoUpdate(UserFinancialInfoBase):
    pass


class UserFinancialInfoRead(UserFinancialInfoBase):
    id: Optional[uuid.UUID]
    iban: Optional[str]
    housing_payments_iban: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True

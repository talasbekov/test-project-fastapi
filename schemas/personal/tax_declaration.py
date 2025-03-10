import datetime
from typing import Optional
from schemas import Model


class TaxDeclarationBase(Model):
    year: str
    is_paid: bool
    profile_id: str


class TaxDeclarationCreate(TaxDeclarationBase):
    pass


class TaxDeclarationUpdate(TaxDeclarationBase):
    pass


class TaxDeclarationRead(TaxDeclarationBase):
    id: Optional[str]
    year: Optional[str]
    is_paid: Optional[bool]
    profile_id: Optional[str]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True

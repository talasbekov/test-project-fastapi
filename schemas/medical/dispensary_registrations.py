import datetime

from typing import Optional

from pydantic import AnyUrl

from schemas import NamedModel, ReadNamedModel


class DispensaryRegistrationBase(NamedModel):
    initiator: str
    initiatorKZ: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    document_link: Optional[AnyUrl]
    profile_id: str


class DispensaryRegistrationCreate(DispensaryRegistrationBase):
    pass


class DispensaryRegistrationUpdate(DispensaryRegistrationBase):
    pass


class DispensaryRegistrationRead(DispensaryRegistrationBase, ReadNamedModel):
    document_link: Optional[str]
    initiator: Optional[str]
    initiatorKZ: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    profile_id: Optional[str]

    class Config:
        orm_mode = True

import datetime

from typing import Optional

from pydantic import AnyUrl, validator

from schemas import NamedModel, ReadNamedModel


class DispensaryRegistrationBase(NamedModel):
    initiator: str
    initiatorKZ: str
    start_date: datetime.datetime
    end_date: Optional[datetime.datetime]
    document_link: Optional[str]
    profile_id: str

    @validator("document_link")
    def validate_document_link(cls, v):
        if v and not v.startswith(("http://", "https://")):
            raise ValueError("Invalid URL format")
        return v


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
    medical_profile_id: Optional[str]
    profile_id: Optional[str]

    class Config:
        orm_mode = True

import datetime
from typing import Optional, List
from pydantic import validator
from pydantic.networks import AnyUrl

from schemas import CustomBaseModel


class UserLiberationBase(CustomBaseModel):
    reason: str
    reasonKZ: str
    liberation_ids: List
    initiator: str
    initiatorKZ: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    profile_id: str
    document_link: Optional[AnyUrl]

    @validator("document_link", pre=True, always=True)
    def validate_url(cls, v):
        if v and not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("Invalid URL format")
        return v or "https://default.link"


class UserLiberationCreate(UserLiberationBase):
    liberation_ids: Optional[List]


class UserLiberationUpdate(UserLiberationBase):
    liberation_ids: Optional[List]


class UserLiberationRead(UserLiberationBase):
    id: Optional[str]
    reason: Optional[str]
    reasonKZ: Optional[str]
    liberation_ids: Optional[List]
    initiator: Optional[str]
    initiatorKZ: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    profile_id: Optional[str]
    medical_profile_id: Optional[str]

    class Config:
        orm_mode = True

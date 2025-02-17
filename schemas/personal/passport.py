import datetime
import uuid
from typing import Optional

from pydantic import AnyUrl, BaseModel
from pydantic import BaseModel, validator, root_validator



class PassportBase(BaseModel):
    document_number: str
    date_of_issue: datetime.date
    date_to: datetime.date
    document_link: Optional[AnyUrl]
    profile_id: str
    issued_by: str


class PassportCreate(PassportBase):
    pass


class PassportUpdate(BaseModel):
    document_number: Optional[str]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    document_link: Optional[AnyUrl]
    profile_id: Optional[str]
    issued_by: Optional[str]


class PassportRead(PassportBase):
    id: str
    document_number: str
    date_of_issue: datetime.date
    date_to: datetime.date
    document_link: Optional[str]
    issued_by: str
    profile_id: str
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    @validator("document_link", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else "https://10.15.3.180/s3/static/placeholder.jpg"

    class Config:
        orm_mode = True

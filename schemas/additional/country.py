import uuid
from typing import Optional

from pydantic import BaseModel


class CountryBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    pass


class CountryRead(CountryBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

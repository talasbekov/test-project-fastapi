import uuid

from pydantic import BaseModel
from typing import Optional


class LanguageBase(BaseModel):
    name: str


class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(LanguageBase):
    pass


class LanguageRead(LanguageBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True

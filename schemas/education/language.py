import uuid

from pydantic import BaseModel
from typing import Optional


class LanguageBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(LanguageBase):
    pass


class LanguageRead(LanguageBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

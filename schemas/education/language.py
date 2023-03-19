import uuid
from typing import Optional

from pydantic import BaseModel


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

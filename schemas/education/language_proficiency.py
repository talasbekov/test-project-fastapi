import uuid
from typing import Optional

from pydantic import BaseModel

from .language import LanguageRead


class LanguageProficiencyBase(BaseModel):
    level: int
    profile_id: Optional[uuid.UUID]
    language_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class LanguageProficiencyCreate(LanguageProficiencyBase):
    pass


class LanguageProficiencyUpdate(LanguageProficiencyBase):
    pass


class LanguageProficiencyRead(LanguageProficiencyBase):
    language: Optional[LanguageRead]

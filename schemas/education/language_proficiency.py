import uuid
from typing import Optional

from pydantic import BaseModel

from .language import LanguageRead
from .. import Model


class LanguageProficiencyBase(Model):
    level: int
    profile_id: Optional[str]
    language_id: Optional[str]
    document_link: Optional[str]
    educational_profile_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class LanguageProficiencyCreate(LanguageProficiencyBase):
    pass


class LanguageProficiencyUpdate(LanguageProficiencyBase):
    pass


class LanguageProficiencyRead(LanguageProficiencyBase):
    id: str
    language: Optional[LanguageRead]
    educational_profile_id: Optional[str]

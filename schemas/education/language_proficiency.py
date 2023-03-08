import uuid

from pydantic import BaseModel
from typing import Optional


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
    id: Optional[uuid.UUID]
    level: int
    profile_id: Optional[uuid.UUID]
    language_id: Optional[uuid.UUID]


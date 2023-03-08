import uuid

from pydantic import BaseModel
from typing import Optional


class InstitutionBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class InstitutionCreate(InstitutionBase):
    pass


class InstitutionUpdate(InstitutionBase):
    pass


class InstitutionRead(InstitutionBase):
    id: Optional[uuid.UUID]
    name: str

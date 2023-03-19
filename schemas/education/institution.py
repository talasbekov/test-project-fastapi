import uuid
from typing import Optional

from pydantic import BaseModel


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

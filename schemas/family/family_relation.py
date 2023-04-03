import uuid
from typing import Optional

from pydantic import BaseModel


class FamilyRelationBase(BaseModel):
    name: str


class FamilyRelationCreate(FamilyRelationBase):
    pass


class FamilyRelationUpdate(FamilyRelationBase):
    pass


class FamilyRelationRead(FamilyRelationBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True

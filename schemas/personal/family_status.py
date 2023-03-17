import uuid

from typing import Optional

from pydantic import BaseModel


class FamilyStatusBase(BaseModel):
    name: str


class FamilyStatusCreate(FamilyStatusBase):
    pass


class FamilyStatusUpdate(FamilyStatusBase):
    pass


class FamilyStatusRead(FamilyStatusBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True

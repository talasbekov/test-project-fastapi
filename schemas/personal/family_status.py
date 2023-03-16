import uuid

from typing import Optional

from pydantic import BaseModel


class FamilyStatusBase(BaseModel):
    name_kz: str
    name_ru: str


class FamilyStatusCreate(FamilyStatusBase):
    pass


class FamilyStatusUpdate(FamilyStatusBase):
    pass


class FamilyStatusRead(FamilyStatusBase):
    id: Optional[uuid.UUID]
    name_kz: Optional[str]
    name_ru: Optional[str]

    class Config:
        orm_mode = True

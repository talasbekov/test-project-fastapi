import uuid
from typing import Optional

from pydantic import BaseModel


class SportTypeBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SportTypeCreate(SportTypeBase):
    pass


class SportTypeUpdate(SportTypeBase):
    pass


class SportTypeRead(SportTypeBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

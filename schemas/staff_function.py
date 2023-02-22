import uuid
from typing import Optional

from pydantic import BaseModel


class StaffFunctionBase(BaseModel):
    name: str


class StaffFunctionCreate(StaffFunctionBase):
    pass


class StaffFunctionUpdate(StaffFunctionBase):
    pass


class StaffFunctionRead(StaffFunctionBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True

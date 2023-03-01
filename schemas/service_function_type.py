import uuid
from typing import Optional

from pydantic import BaseModel


class ServiceFunctionTypeBase(BaseModel):
    name: str


class ServiceFunctionTypeCreate(ServiceFunctionTypeBase):
    pass


class ServiceFunctionTypeUpdate(ServiceFunctionTypeBase):
    pass


class ServiceFunctionTypeRead(ServiceFunctionTypeBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True

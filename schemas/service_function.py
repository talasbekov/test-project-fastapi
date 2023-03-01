import uuid
from typing import List, Optional

from pydantic import BaseModel


class ServiceFunctionBase(BaseModel):
    name: str
    service_function_type_id: uuid.UUID
    spend_hours_per_week: Optional[int]


class ServiceFunctionCreate(ServiceFunctionBase):
    pass


class ServiceFunctionUpdate(ServiceFunctionBase):
    pass


class UserServiceFunction(BaseModel):
    user_id: uuid.UUID
    service_function_ids: List[uuid.UUID]


class ServiceFunctionRead(ServiceFunctionBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    service_function_type_id: Optional[uuid.UUID]
    spend_hours_per_week: Optional[int]

    class Config:
        orm_mode = True

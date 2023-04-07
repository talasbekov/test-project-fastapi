import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ContractBase(BaseModel):

    type_id: uuid.UUID
    user_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ContractCreate(ContractBase):
    pass


class ContractUpdate(ContractBase):
    pass


class ContractRead(ContractBase):
    id: uuid.UUID

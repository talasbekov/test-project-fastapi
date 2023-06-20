import uuid

from typing import Optional

from pydantic import BaseModel

from schemas import NamedModel, ReadNamedModel


class ContractTypeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ContractTypeCreate(ContractTypeBase):
    pass


class ContractTypeUpdate(ContractTypeBase):
    pass


class ContractTypeRead(ContractTypeBase, ReadNamedModel):
    pass


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

    type: Optional[ContractTypeRead]

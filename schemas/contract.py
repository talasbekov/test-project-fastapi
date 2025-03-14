from typing import Optional, List
from schemas import NamedModel, ReadNamedModel, Model


class ContractTypeBase(NamedModel):
    years: Optional[int]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ContractTypeCreate(ContractTypeBase):
    pass


class ContractTypeUpdate(ContractTypeBase):
    pass


class ContractTypeRead(ContractTypeBase, ReadNamedModel):
    pass


class ContractTypeReadPagination(Model):
    total: Optional[int]
    objects: Optional[List[ContractTypeRead]]


class ContractBase(Model):

    type_id: str
    user_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ContractCreate(ContractBase):
    pass


class ContractUpdate(ContractBase):
    pass


class ContractRead(ContractBase):
    id: str

    type: Optional[ContractTypeRead]

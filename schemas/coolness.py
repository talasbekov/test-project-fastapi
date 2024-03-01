from typing import Optional, Any, List

from schemas import Model, NamedModel, ReadModel, ReadNamedModel, BaseModel


class CoolnessTypeBase(NamedModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CoolnessTypeCreate(CoolnessTypeBase):
    order: Optional[int]
#    percentage: Optional[int]


class CoolnessTypeUpdate(CoolnessTypeBase):
    pass


class CoolnessTypeRead(CoolnessTypeBase, ReadNamedModel):
    pass


class CoolnessTypeReadPagination(BaseModel):
    total: Optional[int]
    objects: Optional[List[CoolnessTypeRead]]


class CoolnessBase(Model):
    coolness_status: Optional[Any]
    type_id: Optional[str]
    user_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CoolnessCreate(CoolnessBase):
    pass


class CoolnessUpdate(CoolnessBase):
    pass


class CoolnessRead(CoolnessBase, ReadModel):
    type: Optional[CoolnessTypeRead]

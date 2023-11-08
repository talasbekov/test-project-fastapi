import uuid
from typing import Optional

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class CoolnessTypeBase(NamedModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CoolnessTypeCreate(CoolnessTypeBase):
    pass


class CoolnessTypeUpdate(CoolnessTypeBase):
    pass


class CoolnessTypeRead(CoolnessTypeBase, ReadNamedModel):
    pass


class CoolnessBase(Model):
    is_assigned: Optional[bool]
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

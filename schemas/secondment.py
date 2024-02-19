import uuid

from typing import Optional

from schemas import NamedModel, ReadNamedModel


class SecondmentBase(NamedModel):
    name: Optional[str]
    user_id: str
    staff_division_id: Optional[str]
    state_body_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SecondmentCreate(SecondmentBase):
    pass


class SecondmentUpdate(SecondmentBase):
    pass


class SecondmentRead(SecondmentBase, ReadNamedModel):
    pass

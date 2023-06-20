import uuid

from typing import Optional

from schemas import NamedModel, ReadNamedModel


class SecondmentBase(NamedModel):
    name: Optional[str]
    user_id: uuid.UUID
    staff_division_id: Optional[uuid.UUID]
    state_body_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SecondmentCreate(SecondmentBase):
    pass


class SecondmentUpdate(SecondmentBase):
    pass


class SecondmentRead(SecondmentBase, ReadNamedModel):
    pass

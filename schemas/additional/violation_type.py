import datetime
import uuid
from typing import Optional

from schemas import NamedModel, ReadNamedModel

class ViolationTypeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ViolationTypeCreate(ViolationTypeBase):
    pass

class ViolationTypeUpdate(ViolationTypeBase):
    pass

class ViolationTypeRead(ViolationTypeBase, ReadNamedModel):
    id: Optional[str]
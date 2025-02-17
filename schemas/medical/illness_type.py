import datetime
import uuid
from typing import Optional

from schemas import NamedModel, ReadNamedModel

class IllnessTypeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class IllnessTypeCreate(IllnessTypeBase):
    pass

class IllnessTypeUpdate(IllnessTypeBase):
    pass

class IllnessTypeRead(IllnessTypeBase, ReadNamedModel):
    id: Optional[str]
import datetime
import uuid
from typing import Optional

from schemas import NamedModel, ReadNamedModel

class ActivityTypeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ActivityTypeCreate(ActivityTypeBase):
    pass

class ActivityTypeUpdate(ActivityTypeBase):
    pass

class ActivityTypeRead(ActivityTypeBase, ReadNamedModel):
    id: Optional[str]
import datetime
import uuid
from typing import Optional

from schemas import NamedModel, ReadNamedModel

class CitizenshipBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CitizenshipCreate(CitizenshipBase):
    pass

class CitizenshipUpdate(CitizenshipBase):
    pass

class CitizenshipRead(CitizenshipBase, ReadNamedModel):
    id: Optional[str]
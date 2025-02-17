import datetime
import uuid
from typing import Optional

from schemas import NamedModel, ReadNamedModel

class RegionBase(NamedModel):
    country_id: Optional[str]
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class RegionCreate(RegionBase):
    pass

class RegionUpdate(RegionBase):
    pass

class RegionRead(RegionBase, ReadNamedModel):
    id: Optional[str]
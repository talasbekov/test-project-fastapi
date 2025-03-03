import datetime
import uuid
from typing import Optional

from schemas import NamedModel, ReadNamedModel

class CityBase(NamedModel):
    is_village: Optional[bool] 
    region_id: Optional[str]
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CityCreate(CityBase):
    pass

class CityUpdate(CityBase):
    pass

class CityRead(CityBase, ReadNamedModel):
    id: Optional[str]
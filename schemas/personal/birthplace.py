from typing import Optional

from schemas import Model
from .region import RegionRead
from .city import CityRead
from schemas import CountryRead

class BirthplaceBase(Model):
    region_id: Optional[str]
    city_id: Optional[str]
    country_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BirthplaceCreate(BirthplaceBase):
    pass

class BirthplaceUpdate(BirthplaceBase):
    pass

class BirthplaceRead(BirthplaceBase):
    id: Optional[str]
    name: Optional[str]
    region: Optional[RegionRead]
    city: Optional[CityRead]
    country: Optional[CountryRead]
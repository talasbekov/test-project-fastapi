import datetime
import uuid
from typing import Optional

from schemas import Model
from .region import RegionRead
from .city import CityRead
from schemas import CountryRead, ReadNamedModel

class BirthplaceBase(Model):
    region_id: Optional[str]
    city_id: Optional[str]
    country_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BirthplaceCreate(BirthplaceBase):
    # def __init__(self, region_id, city_id, country_id):
    #     self.region_id = region_id
    #     self.city_id = city_id
    #     self.country_id = country_id
    pass

class BirthplaceUpdate(BirthplaceBase):
    pass

class BirthplaceRead(BirthplaceBase):
    id: Optional[str]
    name: Optional[str]
    region: Optional[RegionRead]
    city: Optional[CityRead]
    country: Optional[CountryRead]
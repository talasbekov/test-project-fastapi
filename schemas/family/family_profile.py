from typing import Optional, List, Union

from .family import FamilyRead
from .. import Model


class FamilyProfileBase(Model):

    profile_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class FamilyProfileCreate(FamilyProfileBase):
    pass


class FamilyProfileUpdate(FamilyProfileBase):
    pass


class FamilyProfileRead(FamilyProfileBase):

    id: Optional[str]
    profile_id: Optional[str]
    
    family: Union[Optional[List[FamilyRead]], str]

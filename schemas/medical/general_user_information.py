import uuid
from typing import Optional

from pydantic import BaseModel

from models import AgeGroup


class GeneralUserInformationBase(BaseModel):
    height: int
    blood_group: str
    age_group: AgeGroup
    profile_id: uuid.UUID
    weight: int
 
    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class GeneralUserInformationCreate(GeneralUserInformationBase):
    pass


class GeneralUserInformationUpdate(GeneralUserInformationBase):
    pass


class GeneralUserInformationRead(GeneralUserInformationBase):
    id: Optional[uuid.UUID]
    height: Optional[int]
    blood_group: Optional[str]
    age_group: Optional[AgeGroup]
    profile_id: Optional[uuid.UUID]
    weight: Optional[int]

    class Config:
        orm_mode = True

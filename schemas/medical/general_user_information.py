from typing import Optional
from models import AgeGroup
from schemas import CustomBaseModel


class GeneralUserInformationBase(CustomBaseModel):
    height: int
    blood_group: str
    age_group: AgeGroup
    profile_id: str
    weight: int

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class GeneralUserInformationCreate(GeneralUserInformationBase):
    pass


class GeneralUserInformationUpdate(GeneralUserInformationBase):
    pass


class GeneralUserInformationRead(GeneralUserInformationBase):
    id: Optional[str]
    height: Optional[int]
    blood_group: Optional[str]
    age_group: Optional[AgeGroup]
    profile_id: Optional[str]
    weight: Optional[int]

    class Config:
        orm_mode = True

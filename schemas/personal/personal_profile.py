import datetime
import uuid
from typing import List, Optional, Union

from pydantic import BaseModel, validator

from schemas.personal import (BiographicInfoRead, DrivingLicenseRead,
                              IdentificationCardRead, PassportRead,
                              SportAchievementRead, SportDegreeRead,
                              TaxDeclarationRead, UserFinancialInfoRead)

from schemas import ProfileRead, CustomBaseModel


# base
class PersonalProfileBase(CustomBaseModel):
    profile_id: str


# create
class PersonalProfileCreate(PersonalProfileBase):
    pass


# update
class PersonalProfileUpdate(PersonalProfileBase):
    pass


# read
class PersonalProfileRead(PersonalProfileBase):
    id: Optional[str]
    profile_id: Optional[str]
    profile: Optional[ProfileRead]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    identification_card: Union[Optional[IdentificationCardRead], str]
    biographic_info: Optional[BiographicInfoRead]
    driving_license: Optional[DrivingLicenseRead]
    passport: Optional[PassportRead]
    sport_achievements: Optional[List[SportAchievementRead]]
    sport_degrees: Optional[List[SportDegreeRead]]
    tax_declarations: Optional[List[TaxDeclarationRead]]
    user_financial_infos: Optional[List[UserFinancialInfoRead]]

    @validator("sport_achievements", "sport_degrees", pre=True, always=True)
    def sort_by_assignment_date(cls, v):
        if v is None:
            return []
        return sorted(v, key=lambda x: x.assignment_date)

    class Config:
        orm_mode = True
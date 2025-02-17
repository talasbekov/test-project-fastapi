import datetime
import uuid
from typing import List, Optional, Union

from pydantic import BaseModel, validator

from schemas.personal import (BiographicInfoRead, DrivingLicenseRead,
                              IdentificationCardRead, PassportRead,
                              SportAchievementRead, SportDegreeRead,
                              TaxDeclarationRead, UserFinancialInfoRead)

from schemas import ProfileRead


# base
class PersonalProfileBase(BaseModel):
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
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]
    profile_id: Optional[str]
    profile: Optional[ProfileRead]

    identification_card: Union[Optional[IdentificationCardRead], str] = None
    biographic_info: Optional[BiographicInfoRead]
    driving_license: Optional[DrivingLicenseRead] = None
    passport: Optional[PassportRead]
    sport_achievements: Optional[List[SportAchievementRead]]
    sport_degrees: Optional[List[SportDegreeRead]]
    tax_declarations: Optional[List[TaxDeclarationRead]]
    user_financial_infos: Optional[List[UserFinancialInfoRead]]

    @validator("sport_achievements", "sport_degrees")
    def sort_by_assignment_date(cls, v):
        return sorted(v, key=lambda x: x.assignment_date)

    class Config:
        orm_mode = True
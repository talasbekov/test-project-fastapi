import datetime
from typing import List, Optional, Union

from schemas.personal import (BiographicInfoRead, DrivingLicenseRead,
                              IdentificationCardRead, PassportRead,
                              SportAchievementRead, SportDegreeRead,
                              TaxDeclarationRead, UserFinancialInfoRead)

from schemas import ProfileRead, Model


class PersonalProfileBase(Model):
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

    class Config:
        orm_mode = True
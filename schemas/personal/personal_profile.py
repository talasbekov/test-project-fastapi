import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel

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

    identification_card: Optional[IdentificationCardRead]
    biographic_info: Optional[BiographicInfoRead]
    driving_license: Optional[DrivingLicenseRead]
    passport: Optional[PassportRead]
    sport_achievements: Optional[List[SportAchievementRead]]
    sport_degrees: Optional[List[SportDegreeRead]]
    tax_declarations: Optional[List[TaxDeclarationRead]]
    user_financial_infos: Optional[List[UserFinancialInfoRead]]

    class Config:
        orm_mode = True

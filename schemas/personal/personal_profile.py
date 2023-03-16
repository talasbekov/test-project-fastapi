import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel

from schemas.personal import (BiographicInfoRead, DrivingLicenseRead,
                              IdentificationCardRead, PassportRead,
                              SportAchievementRead, SportDegreeRead,
                              TaxDeclarationRead, UserFinancialInfoRead)


# base
class PersonalProfileBase(BaseModel):
    profile_id: uuid.UUID


# create
class PersonalProfileCreate(PersonalProfileBase):
    pass


# update
class PersonalProfileUpdate(PersonalProfileBase):
    pass


# read
class PersonalProfileRead(PersonalProfileBase):
    id: Optional[uuid.UUID]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

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

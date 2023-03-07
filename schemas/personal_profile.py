import uuid
import datetime

from typing import Optional, List

from pydantic import BaseModel


# base
class PersonalProfileBase(BaseModel):
    profile_id: uuid.UUID


class BiographicInfoBase(BaseModel):
    place_birth: datetime.date
    gender: bool
    citizenship: str
    nationality: str
    family_status: str
    address: str
    profile_id: uuid.UUID


class UserFinancialInfoBase(BaseModel):
    iban: str
    housing_payments_iban: str
    profile_id: uuid.UUID


class TaxDeclarationBase(BaseModel):
    year: str
    is_paid: bool
    profile_id: uuid.UUID


class SportDegreeBase(BaseModel):
    name: str
    assignment_date: datetime.date
    document_link: str
    profile_id: uuid.UUID


class SportAchievementBase(BaseModel):
    name: str
    assignment_date: datetime.date
    document_link: str
    profile_id: uuid.UUID


class IdentificationCardBase(BaseModel):
    document_number: str
    date_of_issue: datetime.date
    date_to: datetime.date
    issued_by: str
    document_link: str
    profile_id: uuid.UUID


class DrivingLicenceBase(BaseModel):
    document_number: str
    category: List[str]
    date_of_issue: datetime.date
    date_to: datetime.date
    document_link: str
    profile_id: uuid.UUID


class PassportBase(BaseModel):
    document_number: str
    date_of_issue: datetime.date
    date_to: datetime.date
    document_link: str
    profile_id: uuid.UUID


# create
class PersonalProfileCreate(PersonalProfileBase):
    pass


class BiographicInfoCreate(BiographicInfoBase):
    pass


class UserFinancialInfoCreate(UserFinancialInfoBase):
    pass


class TaxDeclarationCreate(TaxDeclarationBase):
    pass


class SportDegreeCreate(SportDegreeBase):
    pass


class SportAchievementCreate(SportAchievementBase):
    pass


class IdentificationCardCreate(IdentificationCardBase):
    pass


class DrivingLicenceCreate(DrivingLicenceBase):
    pass


class PassportCreate(PassportBase):
    pass


# update
class PersonalProfileUpdate(PersonalProfileBase):
    pass


class BiographicInfoUpdate(BiographicInfoBase):
    pass


class UserFinancialInfoUpdate(UserFinancialInfoBase):
    pass


class TaxDeclarationUpdate(TaxDeclarationBase):
    pass


class SportDegreeUpdate(SportDegreeBase):
    pass


class SportAchievementUpdate(SportAchievementBase):
    pass


class IdentificationCardUpdate(IdentificationCardBase):
    pass


class DrivingLicenceUpdate(DrivingLicenceBase):
    pass


class PassportUpdate(PassportBase):
    pass


# read
class PersonalProfileRead(PersonalProfileBase):
    id: Optional[uuid.UUID]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True


class BiographicInfoRead(BiographicInfoBase):
    id: Optional[uuid.UUID]
    place_birth: Optional[datetime.date]
    gender: Optional[bool]
    citizenship: Optional[str]
    nationality: Optional[str]
    family_status: Optional[str]
    address: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True


class UserFinancialInfoRead(UserFinancialInfoBase):
    id: Optional[uuid.UUID]
    iban: Optional[str]
    housing_payments_iban: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True


class TaxDeclarationRead(TaxDeclarationBase):
    id: Optional[uuid.UUID]
    year: Optional[str]
    is_paid: Optional[bool]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True


class SportDegreeRead(SportDegreeBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    assignment_date: Optional[datetime.date]
    document_link: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True


class SportAchievementRead(SportAchievementBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    assignment_date: Optional[datetime.date]
    document_link: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True


class IdentificationCardRead(IdentificationCardBase):
    id: Optional[uuid.UUID]
    document_number: Optional[str]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    issued_by: Optional[str]
    document_link: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True


class DrivingLicenceRead(DrivingLicenceBase):
    id: Optional[uuid.UUID]
    document_number: Optional[str]
    category: Optional[List[str]]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    document_link: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True


class PassportRead(PassportBase):
    id: Optional[uuid.UUID]
    document_number: Optional[str]
    date_of_issue: Optional[datetime.date]
    date_to: Optional[datetime.date]
    document_link: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True

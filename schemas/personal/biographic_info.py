import datetime
import uuid
from typing import Optional, Any

from pydantic import BaseModel, validator, root_validator

from .family_status import FamilyStatusRead
from .citizenship import CitizenshipRead
from .nationality import NationalityRead
from .birthplace import BirthplaceRead


class BiographicInfoBase(BaseModel):
    gender: bool
    family_status_id: str
    address: str
    residence_address: str
    profile_id: str
    citizenship_id: Optional[str]
    nationality_id: Optional[str]
    birthplace_id: Optional[str]


class BiographicInfoCreate(BaseModel):
    gender: bool
    family_status_id: str
    address: str
    residence_address: str
    user_id: Optional[str]
    personal_profile_id: str
    citizenship_id: Optional[str]
    nationality_id: Optional[str]
    region_id: Optional[str]
    city_id: Optional[str]
    country_id: Optional[str]


class BiographicInfoUpdate(BaseModel):
    gender: Optional[bool]
    family_status_id: Optional[str]
    residence_address: Optional[str]
    address: Optional[str]
    user_id: Optional[str]
    profile_id: Optional[str]
    personal_profile_id: Optional[str]
    citizenship_id: Optional[str]
    nationality_id: Optional[str]
    region_id: Optional[str]
    city_id: Optional[str]
    country_id: Optional[str]


class BiographicInfoRead(BiographicInfoBase):
    id: Optional[str]
    gender: Optional[bool]
    family_status_id: Optional[str]
    address: Optional[str]
    residence_address: Optional[str]
    profile_id: Optional[str]
    personal_profile_id: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    family_status: Optional[Any]
    citizenship_id: Optional[str]
    nationality_id: Optional[str]
    citizenship: Optional[Any]
    nationality: Optional[Any]  
    birthplace: Optional[BirthplaceRead]

    class Config:
        orm_mode = True
    
    @validator("address", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else " "

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            gender=orm_obj.gender,
            family_status_id=orm_obj.family_status_id if orm_obj.family_status_id else orm_obj.id,
            address=orm_obj.address,
            residence_address=orm_obj.residence_address,
            profile_id=orm_obj.profile_id,
            personal_profile_id=orm_obj.personal_profile_id,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
            family_status=orm_obj.family_status if orm_obj.family_status else {},
            citizenship_id=orm_obj.citizenship_id,
            birthplace_id=orm_obj.birthplace_id if orm_obj.birthplace_id else orm_obj.id,
            nationality_id=orm_obj.nationality_id if orm_obj.nationality_id else orm_obj.id,
            citizenship=orm_obj.citizenship if orm_obj.citizenship else {},
            nationality=orm_obj.nationality if orm_obj.nationality else {},
            birthplace=orm_obj.birthplace if orm_obj.birthplace else {}
        )

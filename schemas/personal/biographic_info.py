from typing import Optional

from schemas import Model, ReadModel
from schemas.personal import BirthplaceRead, NationalityRead, CitizenshipRead, FamilyStatusRead


# --------------------------
# 1. Модели для создания и обновления
# --------------------------

class BiographicInfoCreate(Model):
    gender: Optional[bool]
    family_status_id: Optional[str]
    address: Optional[str]
    residence_address: Optional[str]
    user_id: Optional[str]
    profile_id: Optional[str]
    citizenship_id: Optional[str]
    nationality_id: Optional[str]

    # Поля для места рождения
    region_id: Optional[str]
    city_id: Optional[str]
    country_id: Optional[str]


class BiographicInfoUpdate(Model):
    gender: Optional[bool]
    family_status_id: Optional[str]
    address: Optional[str]
    residence_address: Optional[str]
    profile_id: Optional[str]
    user_id: Optional[str]
    personal_profile_id: Optional[str]
    citizenship_id: Optional[str]
    nationality_id: Optional[str]
    region_id: Optional[str]
    city_id: Optional[str]
    country_id: Optional[str]


class BiographicInfoRead(ReadModel):
    gender: Optional[bool]
    family_status_id: Optional[str]
    family_status: Optional["FamilyStatusRead"]
    address: Optional[str]
    residence_address: Optional[str]
    profile_id: Optional[str]
    personal_profile_id: Optional[str]
    citizenship_id: Optional[str]
    citizenship: Optional["CitizenshipRead"]
    nationality_id: Optional[str]
    nationality: Optional["NationalityRead"]
    birthplace_id: Optional[str]
    birthplace: Optional["BirthplaceRead"]

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            gender=orm_obj.gender,
            family_status_id=orm_obj.family_status_id,
            family_status=FamilyStatusRead.from_orm(orm_obj.family_status) if orm_obj.family_status else None,
            address=orm_obj.address,
            residence_address=orm_obj.residence_address,
            profile_id=orm_obj.profile_id,
            personal_profile_id=orm_obj.personal_profile_id,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
            citizenship_id=orm_obj.citizenship_id,
            citizenship=CitizenshipRead.from_orm(orm_obj.citizenship) if orm_obj.citizenship else None,
            nationality_id=orm_obj.nationality_id,
            nationality=NationalityRead.from_orm(orm_obj.nationality) if orm_obj.nationality else None,
            birthplace_id=orm_obj.birthplace_id,
            birthplace=BirthplaceRead.from_orm(orm_obj.birthplace) if orm_obj.birthplace else None
        )

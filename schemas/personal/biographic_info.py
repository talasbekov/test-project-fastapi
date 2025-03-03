# schemas/personal/biographic_info.py
from pydantic import Field, validator
from typing import Optional, Dict
import uuid
import datetime

from schemas import CustomBaseModel

# --------------------------
# 1. Модели для создания и обновления
# --------------------------

class BiographicInfoCreate(CustomBaseModel):
    gender: Optional[bool] = None
    family_status_id: Optional[str] = None
    address: Optional[str] = None
    residence_address: Optional[str] = None
    user_id: Optional[str] = None
    personal_profile_id: Optional[str] = None
    citizenship_id: Optional[str] = None
    nationality_id: Optional[str] = None

    # Поля для места рождения
    region_id: Optional[str] = None
    city_id: Optional[str] = None
    country_id: Optional[str] = None


class BiographicInfoUpdate(CustomBaseModel):
    gender: Optional[bool] = None
    family_status_id: Optional[str] = None
    address: Optional[str] = None
    residence_address: Optional[str] = None
    profile_id: Optional[str] = None
    user_id: Optional[str] = None
    personal_profile_id: Optional[str] = None
    citizenship_id: Optional[str] = None
    nationality_id: Optional[str] = None
    region_id: Optional[str] = None
    city_id: Optional[str] = None
    country_id: Optional[str] = None


# --------------------------
# 2. Функции значений по умолчанию
# --------------------------

def default_family_status() -> Dict:
    return {
        "id": "missing_family_status",
        "name": "Данные отсутствуют!",
        "nameKZ": "Данные отсутствуют!",
        "created_at": datetime.datetime(1920, 1, 1),
        "updated_at": datetime.datetime(1920, 1, 1),
    }

def default_citizenship() -> Dict:
    return {
        "id": "missing_citizenship",
        "name": "Данные отсутствуют!",
        "nameKZ": "Данные отсутствуют!",
        "created_at": datetime.datetime(1920, 1, 1),
        "updated_at": datetime.datetime(1920, 1, 1),
    }

def default_nationality() -> Dict:
    return {
        "id": "missing_nationality",
        "name": "Данные отсутствуют!",
        "nameKZ": "Данные отсутствуют!",
        "created_at": datetime.datetime(1920, 1, 1),
        "updated_at": datetime.datetime(1920, 1, 1),
    }

# Обновлённые функции для регионов, городов и стран
def default_region() -> Dict:
    return {
        "id": "missing_region",
        "created_at": datetime.datetime(1920, 1, 1),
        "updated_at": datetime.datetime(1920, 1, 1),
        "name": "Данные отсутствуют!",
        "nameKZ": "Данные отсутствуют!",
        "country_id": "missing_country"
    }

def default_city() -> Dict:
    return {
        "id": "missing_city",
        "created_at": datetime.datetime(1920, 1, 1),
        "updated_at": datetime.datetime(1920, 1, 1),
        "name": "Данные отсутствуют!",
        "nameKZ": "Данные отсутствуют!",
        "is_village": False,
        "region_id": "missing_region"
    }

def default_country() -> Dict:
    return {
        "id": "missing_country",
        "created_at": datetime.datetime(1920, 1, 1),
        "updated_at": datetime.datetime(1920, 1, 1),
        "name": "Данные отсутствуют!",
        "nameKZ": "Данные отсутствуют!"
    }

def default_birthplace() -> Dict:
    return {
        "id": "missing_birthplace",
        "region_id": "missing_region",
        "city_id": "missing_city",
        "country_id": "missing_country",
        "name": "Данные отсутствуют!",
        "created_at": datetime.datetime(1920, 1, 1),
        "updated_at": datetime.datetime(1920, 1, 1),
        "region": default_region(),
        "city": default_city(),
        "country": default_country(),
    }

def complete_dict(default: Dict, data: Optional[Dict]) -> Dict:
    if not isinstance(data, dict):
        return default
    merged = default.copy()
    merged.update(data)
    return merged

def default_date(
    value: Optional[datetime.datetime],
    default: datetime.datetime = datetime.datetime(1920, 1, 1)
) -> datetime.datetime:
    return value if isinstance(value, datetime.datetime) else default


# --------------------------
# 3. Модель для чтения (ответ API)
# --------------------------

class BiographicInfoRead(CustomBaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    gender: bool = False
    family_status_id: str = "missing_family_status"
    address: str = "Данные отсутствуют!"
    residence_address: str = "Данные отсутствуют!"
    profile_id: str = "missing_profile"
    personal_profile_id: str = "missing_personal_profile"
    citizenship_id: str = "missing_citizenship_id"
    nationality_id: str = "missing_nationality_id"
    birthplace_id: str = "missing_birthplace_id"

    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime(1920, 1, 1))
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime(1920, 1, 1))

    # Связанные объекты
    family_status: Dict = Field(default_factory=default_family_status)
    citizenship: Dict = Field(default_factory=default_citizenship)
    nationality: Dict = Field(default_factory=default_nationality)
    birthplace: Dict = Field(default_factory=default_birthplace)

    class Config:
        orm_mode = True

    @validator("id", pre=True, always=True)
    def validate_id(cls, v):
        return v or str(uuid.uuid4())

    @validator(
        "family_status_id", "profile_id", "citizenship_id", "nationality_id", "birthplace_id",
        pre=True, always=True
    )
    def validate_missing_strings(cls, v):
        return v or "Данные отсутствуют!"

    @validator("address", "residence_address", pre=True, always=True)
    def validate_address(cls, v):
        return v or "Данные отсутствуют!"

    @validator("created_at", "updated_at", pre=True, always=True)
    def validate_dates(cls, v):
        return default_date(v)

    @validator("family_status", pre=True, always=True)
    def validate_family_status(cls, v):
        return complete_dict(default_family_status(), v)

    @validator("citizenship", pre=True, always=True)
    def validate_citizenship(cls, v):
        return complete_dict(default_citizenship(), v)

    @validator("nationality", pre=True, always=True)
    def validate_nationality(cls, v):
        return complete_dict(default_nationality(), v)

    @validator("birthplace", pre=True, always=True)
    def validate_birthplace(cls, v):
        return complete_dict(default_birthplace(), v)

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id or str(uuid.uuid4()),
            gender=orm_obj.gender if orm_obj.gender is not None else False,
            family_status_id=orm_obj.family_status_id or "missing_family_status",
            address=orm_obj.address or "Данные отсутствуют!",
            residence_address=orm_obj.residence_address or "Данные отсутствуют!",
            profile_id=orm_obj.profile_id or "missing_profile",
            personal_profile_id=orm_obj.personal_profile_id or "missing_personal_profile",
            created_at=orm_obj.created_at or datetime.datetime(1920, 1, 1),
            updated_at=orm_obj.updated_at or datetime.datetime(1920, 1, 1),
            family_status=(orm_obj.family_status.dict() if hasattr(orm_obj.family_status, "dict") else orm_obj.family_status) or default_family_status(),
            citizenship_id=orm_obj.citizenship_id or "missing_citizenship_id",
            nationality_id=orm_obj.nationality_id or "missing_nationality_id",
            birthplace_id=orm_obj.birthplace_id or "missing_birthplace_id",
            citizenship=(orm_obj.citizenship.dict() if hasattr(orm_obj.citizenship, "dict") else orm_obj.citizenship) or default_citizenship(),
            nationality=(orm_obj.nationality.dict() if hasattr(orm_obj.nationality, "dict") else orm_obj.nationality) or default_nationality(),
            birthplace=(orm_obj.birthplace.dict() if hasattr(orm_obj.birthplace, "dict") else orm_obj.birthplace) or default_birthplace()
        )

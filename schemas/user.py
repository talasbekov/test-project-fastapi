import datetime
import uuid
from typing import List, Optional

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, EmailStr, Field, root_validator, validator

# Импорт нужных схем
from schemas import (
    BadgeRead,
    RankRead,
    ShortUserStaffUnitRead,
    StaffUnitReadActive,
    StatusRead
)
from schemas import Model, ReadModel
from schemas.base import Model


def calculate_age_from_birthdate(birth_date: datetime.date) -> int:
    today = datetime.datetime.now()
    age = relativedelta(today, birth_date)
    return age.years

def get_age_group(age: int) -> int:
    """
    Возвращает код возрастной категории по возрасту:
    1 — до 25,
    2 — 25-29,
    3 — 30-34,
    4 — 35-39,
    5 — 40-44,
    6 — 45-49,
    0 — 50 и старше.
    """
    if age <= 25:
        return 1
    elif age < 30:
        return 2
    elif age < 35:
        return 3
    elif age < 40:
        return 4
    elif age < 45:
        return 5
    elif age < 50:
        return 6
    else:
        return 0

# Пример модели UserBase, наследующей и от вашего Model, и от Model
class UserBase(Model):
    """
    Общие поля для пользователя
    """
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    father_name: Optional[str]
    staff_unit_id: Optional[str]
    actual_staff_unit_id: Optional[str]
    icon: Optional[str]
    call_sign: Optional[str]
    id_number: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    cabinet: Optional[str]
    service_phone_number: Optional[str]
    supervised_by: Optional[str]
    is_military: Optional[bool]
    personal_id: Optional[str]
    date_birth: Optional[datetime.datetime]
    iin: Optional[str]
    is_active: Optional[bool]
    description: Optional[str]

    @validator(
        "father_name", "description", "address", "cabinet",
        "call_sign", "id_number", "phone_number", "service_phone_number",
        "supervised_by", pre=True, always=True
    )
    def default_empty_string(cls, v):
        return v if v is not None else "Данные отсутствуют!"

    @validator("iin", pre=True, always=True)
    def default_empty_iin(cls, v):
        return v if v is not None else "Данные отсутствуют!"

    @validator("email", pre=True, always=True)
    def ensure_email(cls, v):
        return v if v is not None else "fake@example.com"

class UserCreate(UserBase):
    password: Optional[str] = None

class UserUpdate(UserBase):
    id: Optional[str]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    iin: Optional[str]

class UserGroupUpdate(Model):
    user_id: str
    group_id: str

class UserReadDocumentShort(UserBase, ReadModel):
    last_signed_at: Optional[datetime.datetime]
    statuses: Optional[List[StatusRead]] = Field(default_factory=list)
    staff_unit: Optional[ShortUserStaffUnitRead]
    actual_staff_unit: Optional[ShortUserStaffUnitRead]
    rank: Optional[RankRead]

    class Config:
        orm_mode = True

class UserRead(UserBase, ReadModel):
    badges: Optional[List[BadgeRead]] = Field(default_factory=list)
    is_military: Optional[bool]
    last_signed_at: Optional[datetime.datetime]
    status_till: Optional[datetime.datetime]
    statuses: Optional[List[StatusRead]] = Field(default_factory=list)
    staff_unit: Optional[ShortUserStaffUnitRead]
    actual_staff_unit: Optional[ShortUserStaffUnitRead]
    rank: Optional[RankRead]

    class Config:
        orm_mode = True

class UserReadActiveShort(ReadModel):
    staff_unit: Optional[StaffUnitReadActive]
    first_name: Optional[str]
    last_name: Optional[str]
    last_signed_at: Optional[datetime.datetime]
    staff_unit_id: Optional[str]
    statuses: Optional[List[StatusRead]]
    icon: Optional[str] = ""

    class Config:
        orm_mode = True
        extra = "ignore"  # Игнорируем дополнительные поля, такие как badges

    @validator("first_name", "last_name", "icon", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else "Данные отсутствуют!"

class UserShortRead(Model):
    id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    icon: Optional[str]
    rank: Optional[RankRead]
    staff_unit_id: Optional[str]
    iin: Optional[str]
    email: Optional[EmailStr]

    class Config:
        orm_mode = True

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v if v else str(uuid.uuid4())

    @validator("first_name", "last_name", "father_name", "icon", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else "Данные отсутствуют!"

    @validator("iin", pre=True, always=True)
    def default_empty_iin(cls, v):
        return v if v is not None else "Данные отсутствуют!"

    @validator("email", pre=True, always=True)
    def default_empty_email(cls, v):
        return v if v is not None else "fake@example.com"

class UserShortReadPagination(Model):
    total: int = Field(0, nullable=False)
    objects: List[UserShortRead] = Field(default_factory=list, nullable=False)

class UserShortReadStatus(Model):
    id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    icon: Optional[str]
    rank: Optional[RankRead]
    statuses: Optional[List[StatusRead]]

    class Config:
        orm_mode = True

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v if v else str(uuid.uuid4())

    @validator("first_name", "last_name", "father_name", "icon", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else "Данные отсутствуют!"

class UserShortReadAgeCategory(Model):
    id: Optional[uuid.UUID]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    icon: Optional[str]
    rank: Optional[RankRead]
    date_birth: Optional[datetime.date]
    staff_division: Optional[dict]
    age_category: Optional[int]

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, orm_obj):
        staff_division = getattr(orm_obj.staff_unit, "staff_division", None)
        birth_date = getattr(orm_obj, "date_birth", None)
        if birth_date and isinstance(birth_date, datetime.date):
            age = calculate_age_from_birthdate(birth_date)
            age_cat = get_age_group(age)
        else:
            age_cat = None
        return cls(
            id=orm_obj.id,
            first_name=orm_obj.first_name,
            last_name=orm_obj.last_name,
            father_name=orm_obj.father_name,
            icon=orm_obj.icon,
            rank=orm_obj.rank,
            date_birth=birth_date,
            staff_division={
                "name": staff_division.name if staff_division else None,
                "nameKZ": staff_division.nameKZ if staff_division else None,
            } if staff_division else None,
            age_category=age_cat
        )

class TableUserRead(Model):
    total: int
    users: List[UserRead]

class TableUserReadActive(Model):
    total: int
    users: List[UserReadActiveShort]

class UserShortReadFullNames(Model):
    total: int
    users: List[UserShortRead]

class UserShortReadStatusPagination(Model):
    total: int = Field(0, nullable=False)
    objects: List[UserShortReadStatus] = Field(default_factory=list, nullable=False)

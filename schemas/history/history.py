import uuid
from enum import Enum
from decimal import Decimal
from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from datetime import datetime, timezone, timedelta, date
from typing import Optional, List, Union, Dict, Any, get_origin, get_args
from uuid import UUID

from models import ServiceIDStatus
from .general_information import GeneralInformationRead
from schemas import (
    Model,
    ReadModel,
    ReadNamedModel,
    PositionRead,
    RankRead,
    UserRead,
    PenaltyRead,
    SecondmentRead,
    StatusRead,
    CoolnessRead,
    ContractRead,
    BadgeRead,
    StaffDivisionReadWithoutStaffUnit,
    DrivingLicenseRead,
    IdentificationCardRead,
    PassportRead,
    AcademicDegreeShorRead,
    AcademicTitleShortRead,
    CourseShortRead,
    EducationShortRead,
    StaffDivisionRead
)
from .history_personal import (
    PenaltyReadHistory,
    WorkExperienceRead,
    EmergencyServiceRead,
    AttestationReadHistory,
    NameChangeReadHistory,
    StatusReadHistory,
    CoolnessReadHistory,
    SecondmentReadHistory,
    ContractReadHistory,
    BadgeReadHistory,
)
from ..base import Model

# Set time_zone to UTC(+06:00)
time_zone = timezone(timedelta(hours=6))


class StatusEnum(Enum):
    granted = "Присвоен"
    confirmed = "Подтвержден"
    canceled = "Отменен"


def is_valid_uuid(uuid_str):
    try:
        uuid_obj = UUID(uuid_str, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_str


def get_date_difference(date1: date, date2: date) -> Dict[str, int]:
    difference = date2 - date1
    years = difference.days // 365
    remaining_days = difference.days % 365
    months = remaining_days // 30
    days = remaining_days % 30
    return {"years": years, "months": months, "days": days}


def get_status(obj, confirm_document_link, cancel_document_link):
    if obj is not None:
        status = StatusEnum.granted
        if confirm_document_link is not None:
            status = StatusEnum.confirmed
        if cancel_document_link is not None:
            status = StatusEnum.canceled
        dict_obj = obj.dict()
        dict_obj["status"] = status
        return dict_obj
    else:
        return None


def get_default_for_type(field_type: Any) -> Any:
    """
    Возвращает значение по умолчанию для заданного типа.
    Обрабатывает как простые типы, так и Optional (Union[тип, NoneType]).
    """
    defaults = {
        str: "Не указано",
        int: 0,
        Decimal: Decimal("0.00"),
        bool: False,
        datetime: datetime(1920, 1, 1, tzinfo=timezone.utc),
        date: date(1920, 1, 1),
    }
    origin = get_origin(field_type)
    if origin is Union:
        args = get_args(field_type)
        for typ in args:
            if typ in defaults:
                return defaults[typ]
        return "Не указано"
    else:
        return defaults.get(field_type, "Не указано")


class HistoryBase(Model):
    document_link: Optional[str]
    cancel_document_link: Optional[str]
    confirm_document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    position_id: Optional[str]
    position_name: Optional[str]
    position_nameKZ: Optional[str]
    actual_position_id: Optional[str]
    actual_position_name: Optional[str]
    actual_position_nameKZ: Optional[str]
    rank_id: Optional[str]
    penalty_id: Optional[str]
    emergency_service_id: Optional[str]
    secondment_id: Optional[str]
    name_change_id: Optional[str]
    attestation_id: Optional[str]
    characteristic_initiator_id: Optional[str]
    rank_assigned_by: Optional[str]
    status_id: Optional[str]
    status_name: Optional[str]
    coolness_id: Optional[str]
    contract_id: Optional[str]
    badge_id: Optional[str]
    user_id: str
    is_credited: Optional[bool]
    document_style: Optional[str]
    date_credited: Optional[datetime]
    name_of_organization: Optional[str]
    name_of_organizationKZ: Optional[str] = Field(alias='name_of_organizationKZ', default="")
    type: Optional[str]
    position_work_experience: Optional[str]
    position_work_experienceKZ: Optional[str] = Field(alias='position_work_experienceKZ', default="")
    staff_division_id: Optional[str]
    coefficient: Optional[Decimal]
    percentage: Optional[int]
    staff_division_name: Optional[str]
    staff_division_nameKZ: Optional[str]
    contractor_signer_name: Optional[str]
    contractor_signer_nameKZ: Optional[str]
    reason: Optional[str]
    reasonKZ: Optional[str]
    early_promotion: Optional[bool]
    is_sgo: Optional[bool]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class HistoryCreate(HistoryBase):
    pass


class HistoryContractCreate(Model):
    user_id: str
    type: str
    date_from: datetime
    date_to: Optional[datetime]
    document_number: str
    contract_type_id: str
    experience_years: Optional[int]
    date_credited: Optional[datetime]


class HistoryBadgeCreate(Model):
    user_id: str
    type: str
    date_from: datetime
    date_to: Optional[datetime]
    document_number: str
    badge_type_id: str
    reason: str
    reasonKZ: str
    url: str


class HistoryRankCreate(Model):
    user_id: str
    type: str = "rank_history"
    early_promotion: Optional[bool] = False
    date_from: datetime
    document_number: str
    rank_id: str
    rank_assigned_by: Optional[str]


class HistorySecondmentCreate(Model):
    user_id: str
    type: str
    date_from: datetime
    date_to: Optional[datetime]
    document_number: str
    staff_division_id: Optional[str]
    value: Optional[str]


class HistoryPenaltyCreate(Model):
    user_id: str
    type: str
    date_from: datetime
    date_to: Optional[datetime]
    document_number: str
    penalty_type_id: str
    reason: str
    reasonKZ: str


class HistoryStatusCreate(Model):
    user_id: str
    type: str
    date_from: datetime
    date_to: Optional[datetime]
    document_number: str
    status_type_id: str


class HistoryCoolnessCreate(Model):
    user_id: str
    type: str
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_number: Optional[str]
    coolness_type_id: str
    coolness_status: str


class HistoryBlackBeretCreate(Model):
    user_id: str
    type: str
    date_from: Optional[datetime]
    document_number: Optional[str]


class HistoryAttestationCreate(Model):
    user_id: str
    type: str
    date_from: datetime
    date_to: Optional[datetime]
    document_number: str
    date_credited: Optional[datetime]
    attestation_status: str
    attestation_statusKZ: str


class HistoryUpdate(HistoryBase):
    type: Optional[str]
    attestation_reg_number: Optional[str]
    attestation_status: Optional[str]
    attestation_statusKZ: Optional[str]
    badge_type_id: Optional[str]
    status_type_id: Optional[str]
    experience_years: Optional[int]
    url: Optional[str]
    rank_type_id: Optional[str]


class HistoryRead(HistoryBase, ReadNamedModel):
    rank: Optional[RankRead]
    position: Optional[PositionRead]
    penalty: Optional[PenaltyRead]
    secondment: Optional[SecondmentRead]
    status: Optional[StatusRead]
    coolness: Optional[CoolnessRead]
    contract: Optional[ContractRead]
    badge: Optional[BadgeRead]
    staff_division: Optional[StaffDivisionReadWithoutStaffUnit]
    user_id: Optional[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @property
    def coolness_status(self) -> Optional[dict]:
        return get_status(self.coolness, self.confirm_document_link, self.cancel_document_link)

    @property
    def badge_status(self) -> Optional[dict]:
        return get_status(self.badge, self.confirm_document_link, self.cancel_document_link)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "nameKZ": self.nameKZ,
            "document_link": self.document_link,
            "confirm_document_link": self.confirm_document_link,
            "cancel_document_link": self.cancel_document_link,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "position_id": self.position_id,
            "rank_id": self.rank_id,
            "penalty_id": self.penalty_id,
            "emergency_service_id": self.emergency_service_id,
            "secondment_id": self.secondment_id,
            "name_change_id": self.name_change_id,
            "attestation_id": self.attestation_id,
            "characteristic_initiator_id": self.characteristic_initiator_id,
            "rank_assigned_by": self.rank_assigned_by,
            "status_id": self.status_id,
            "status_name": self.status_name,
            "coolness_id": self.coolness_id,
            "contract_id": self.contract_id,
            "badge_id": self.badge_id,
            "user_id": self.user_id,
            "is_credited": self.is_credited,
            "document_style": self.document_style,
            "date_credited": self.date_credited,
            "name_of_organization": self.name_of_organization,
            "name_of_organizationKZ": self.name_of_organizationKZ,
            "position_work_experience": self.position_work_experience,
            "position_work_experienceKZ": self.position_work_experienceKZ,
            "coefficient": self.coefficient,
            "percentage": self.percentage,
            "staff_division_name": self.staff_division_name,
            "staff_division_nameKZ": self.staff_division_nameKZ,
            "position": self.position,
            "rank": self.rank,
            "penalty": self.penalty,
            "secondment": self.secondment,
            "status": self.status,
            "coolness": self.coolness_status,
            "contract": self.contract,
            "document_number": self.document_number,
            "badge": self.badge_status,
            "staff_division": self.staff_division,
            "type": self.type,
        }


class HistoryPersonalRead(ReadModel):
    date_from: Optional[datetime]
    coefficient: Optional[Decimal]
    percentage: Optional[Decimal]
    characteristic_initiator: Optional[UserRead]
    date_to: Optional[datetime]
    position: Optional[PositionRead]
    rank: Optional[RankRead]
    penalty: Optional[PenaltyReadHistory]
    emergency_service: Optional[EmergencyServiceRead]
    work_experience: Optional[WorkExperienceRead]
    secondment: Optional[SecondmentReadHistory]
    name_change: Optional[NameChangeReadHistory]
    attestation: Optional[AttestationReadHistory]
    status: Optional[StatusReadHistory]
    coolness: Optional[CoolnessReadHistory]
    contract: Optional[ContractReadHistory]
    badge: Optional[BadgeReadHistory]
    document_link: Optional[str]
    confirm_document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: Optional[str]
    name_of_organization: Optional[str]
    name_of_organizationKZ: Optional[str]
    position_work_experience: Optional[str]
    position_work_experienceKZ: Optional[str]
    user_id: str
    type: str
    coefficent: Optional[Decimal]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @property
    def service_characteristic(self) -> Optional[dict]:
        if self.characteristic_initiator is not None:
            full_name = f"{self.characteristic_initiator.last_name} {self.characteristic_initiator.first_name}"
            return {"name": full_name, "nameKZ": full_name}
        return None

    @property
    def emergency_service(self) -> Optional[dict]:
        if self.coefficient is not None:
            combined = f"{self.coefficient} {self.percentage}"
            return {"name": combined, "nameKZ": combined}
        return None

    @property
    def work_experience(self) -> Optional[dict]:
        if self.name_of_organization is not None:
            return {"name": self.name_of_organization, "nameKZ": self.name_of_organizationKZ}
        return None

    @property
    def coolness_status(self) -> Optional[dict]:
        return get_status(self.coolness, self.confirm_document_link, self.cancel_document_link)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "position": self.position,
            "rank": self.rank,
            "penalty": self.penalty,
            "emergency_service": self.emergency_service,
            "secondment": self.secondment,
            "name_change": self.name_change,
            "attestation": self.attestation,
            "status": self.status,
            "coolness": self.coolness_status,
            "contract": self.contract,
            "badge": self.badge_status,
            "document_link": self.document_link,
            "confirm_document_link": self.confirm_document_link,
            "cancel_document_link": self.cancel_document_link,
            "document_number": self.document_number,
            "user_id": self.user_id,
            "type": self.type,
            "service_characteristic": self.service_characteristic,
            "work_experience": self.work_experience,
            "name_of_organization": self.name_of_organization,
            "name_of_organizationKZ": self.name_of_organizationKZ,
            "position_work_experience": self.position_work_experience,
            "position_work_experienceKZ": self.position_work_experienceKZ,
        }

    @property
    def badge_status(self) -> Optional[dict]:
        if self.badge:
            status = 'Добавление' if not self.cancel_document_link else 'Лишение'
            badge_dict = self.badge.dict()
            badge_dict["status"] = status
            return badge_dict


class TrainingAttendanceRead(Model):
    physical_training: Optional[int] = None
    tactical_training: Optional[int] = None
    shooting_training: Optional[int] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def fill_none_values(cls, values):
        values = dict(values)
        values["physical_training"] = values.get("physical_training") or 999999
        values["tactical_training"] = values.get("tactical_training") or 999999
        values["shooting_training"] = values.get("shooting_training") or 999999
        return values


class BadgeServiceDetailRead(ReadNamedModel):
    document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    url: Optional[str]
    reason: Optional[str] = Field(default="")
    reasonKZ: Optional[str] = Field(default="")
    badge_order: Optional[int]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            document_link=orm_obj.document_link,
            document_number=orm_obj.document_number,
            cancel_document_link=orm_obj.cancel_document_link,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            name=orm_obj.badge.type.name,
            nameKZ=orm_obj.badge.type.nameKZ,
            badge_order=orm_obj.badge.type.badge_order,
            url=orm_obj.badge.type.url,
            id=orm_obj.id,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
            reason=orm_obj.reason,
            reasonKZ=orm_obj.reasonKZ
        )


class RankServiceDetailRead(ReadNamedModel):
    rank_assigned_by: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_style: Optional[str]
    rank_id: Optional[str]
    early_promotion: Optional[bool]
    rank: Optional[RankRead]
    military_url: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            name=getattr(orm_obj.rank, "name", "Данные отсутствуют!"),
            nameKZ=getattr(orm_obj.rank, "nameKZ", "Данные отсутствуют!"),
            rank_id=getattr(orm_obj.rank, "id", orm_obj.id),
            document_link=orm_obj.document_link,
            rank_assigned_by=orm_obj.rank_assigned_by,
            document_number=orm_obj.document_number,
            document_style=orm_obj.document_style,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            early_promotion=orm_obj.early_promotion or False
        )


class PenaltyRead(Model):
    id: str
    status: Optional[str] = None
    document_link: Optional[str] = None
    document_number: Optional[str] = None
    cancel_document_link: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    reason: Optional[str] = None
    reasonKZ: Optional[str] = None
    penalty_id: Optional[str] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            status=orm_obj.penalty.type.name if orm_obj.penalty.type else None,
            document_link=orm_obj.document_link,
            cancel_document_link=orm_obj.cancel_document_link,
            document_number=orm_obj.document_number,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            reason=orm_obj.reason,
            reasonKZ=orm_obj.reasonKZ,
            penalty_id=orm_obj.penalty_id
        )


class ContractRead(ReadNamedModel):
    contract_id: str
    contract_type_id: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: str
    experience_years: Optional[int]
    date_credited: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        if not is_valid_uuid(orm_obj.id):
            orm_obj.id = str(uuid.uuid4())
        return cls(
            id=orm_obj.id,
            contract_id=orm_obj.contract_id,
            contract_type_id=orm_obj.contract.type_id,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            document_link=orm_obj.document_link,
            cancel_document_link=orm_obj.cancel_document_link,
            document_number=orm_obj.document_number,
            experience_years=orm_obj.experience_years,
            name=orm_obj.contract.type.name,
            nameKZ=orm_obj.contract.type.nameKZ,
            date_credited=orm_obj.date_credited
        )


class AttestationRead(Model):
    id: str
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: Optional[str]
    date_credited: Optional[datetime]
    attestation_status: Optional[str]
    attestation_statusKZ: Optional[str] = Field(default="")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            document_link=orm_obj.document_link or "https://default.link",
            cancel_document_link=orm_obj.cancel_document_link or "https://default.link",
            document_number=orm_obj.document_number or "0000",
            date_credited=orm_obj.date_credited,
            attestation_status=orm_obj.attestation_status or "Не указано",
            attestation_statusKZ=orm_obj.attestation_statusKZ or "Не указано"
        )

    @validator("document_link", "cancel_document_link", "document_number", "attestation_status", "attestation_statusKZ",
               pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else "Не указано"

    @validator("date_from", "date_to", "date_credited", pre=True, always=True)
    def default_date(cls, v):
        return v if v is not None else datetime(1920, 1, 1, tzinfo=timezone.utc)


class CharacteristicRead(ReadModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: Optional[str]
    characteristic_initiator: Optional[str]
    characteristic_initiator_id: Optional[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        crc_init = orm_obj.characteristic_initiator
        full_name = (
            f"{crc_init.last_name} {crc_init.first_name[0]}."
            f"{'' if crc_init.father_name is None else crc_init.father_name[0]}"
            if crc_init else "Не указано"
        )
        return cls(
            id=orm_obj.id,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            document_link=orm_obj.document_link or "https://default.link",
            cancel_document_link=orm_obj.cancel_document_link or "https://default.link",
            document_number=orm_obj.document_number or "0000",
            characteristic_initiator=full_name,
            characteristic_initiator_id=orm_obj.characteristic_initiator_id or "00000000-0000-0000-0000-000000000000"
        )

    @validator("document_link", "cancel_document_link", "document_number", "characteristic_initiator", pre=True,
               always=True)
    def default_empty_string(cls, v):
        return v if v is not None else "Не указано"

    @validator("date_from", "date_to", pre=True, always=True)
    def default_date(cls, v):
        return v if v is not None else datetime(1920, 1, 1, tzinfo=timezone.utc)

    @validator("characteristic_initiator_id", pre=True, always=True)
    def default_uuid(cls, v):
        return v if v is not None else "00000000-0000-0000-0000-000000000000"


class HolidayRead(Model):
    id: str
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: Optional[str]
    status: Optional[str]
    status_type_id: Optional[str]
    status_id: Optional[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            document_link=orm_obj.document_link or "https://default.link",
            cancel_document_link=orm_obj.cancel_document_link or "https://default.link",
            document_number=orm_obj.document_number or "0000",
            status=orm_obj.status.type.name if orm_obj.status and orm_obj.status.type else "Не указано",
            status_type_id=orm_obj.status.type.id if orm_obj.status and orm_obj.status.type else "00000000-0000-0000-0000-000000000000",
            status_id=orm_obj.status.id if orm_obj.status else "00000000-0000-0000-0000-000000000000"
        )

    @validator("document_link", "cancel_document_link", "document_number", "status", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else "Не указано"

    @validator("date_from", "date_to", pre=True, always=True)
    def default_date(cls, v):
        return v if v is not None else datetime(1920, 1, 1, tzinfo=timezone.utc)

    @validator("status_type_id", "status_id", pre=True, always=True)
    def default_uuid(cls, v):
        return v if v is not None else "00000000-0000-0000-0000-000000000000"


class LengthOfServiceRead(Model):
    years: Optional[int]
    months: Optional[int]
    days: Optional[int]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @validator("years", "months", "days", pre=True, always=True)
    def default_values(cls, v, field):
        defaults = {"years": 99, "months": 12, "days": 1}
        return v if v is not None else defaults[field.name]

    def __getitem__(self, key):
        if key in ("years", "months", "days"):
            return getattr(self, key)
        raise KeyError(f"Invalid key: {key}")

    def __setitem__(self, key, value):
        if key in ("years", "months", "days"):
            setattr(self, key, value)
        else:
            raise KeyError(f"Invalid key: {key}")


class EmergencyContractRead(Model):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    length_of_service: Optional[LengthOfServiceRead] = Field(default_factory=LengthOfServiceRead)
    coefficient: Optional[Decimal] = Decimal("0.00")
    percentage: Optional[int] = 100
    staff_division: Optional[dict] = Field(default_factory=dict)
    position: Optional[PositionRead] = None
    position_name: Optional[str] = "Данные отсутствуют!"
    position_nameKZ: Optional[str] = "Данные отсутствуют!"
    actual_position: Optional[dict] = Field(default_factory=dict)
    actual_position_name: Optional[str] = "Данные отсутствуют!"
    actual_position_nameKZ: Optional[str] = "Данные отсутствуют!"
    emergency_rank_id: Optional[str]
    document_link: Optional[str] = "Данные отсутствуют!"
    document_number: Optional[str] = "Данные отсутствуют!"
    document_style: Optional[str] = "Данные отсутствуют!"
    contractor_signer_name: Optional[Union[Dict, str]]
    date_credited: Optional[datetime]
    staff_division_name: Optional[str] = "Данные отсутствуют!"
    staff_division_nameKZ: Optional[str] = "Данные отсутствуют!"
    is_sgo: Optional[bool] = False

    class Config:
        orm_mode = True

    @validator("contractor_signer_name", pre=True, always=True)
    def ensure_dict(cls, v):
        if isinstance(v, str):
            return {"name": v}
        return v or {"name": "Неизвестный подписант"}

    @root_validator(pre=True)
    def fill_none_values(cls, values):
        values = dict(values)
        defaults = {
            "length_of_service": LengthOfServiceRead(years=99, months=12, days=1),
            "coefficient": Decimal("0.00"),
            "percentage": 100,
            "staff_division": {},
            "position": {},
            "actual_position": {},
            "position_name": "Данные отсутствуют!",
            "position_nameKZ": "Данные отсутствуют!",
            "actual_position_name": "Данные отсутствуют!",
            "actual_position_nameKZ": "Данные отсутствуют!",
            "document_link": "Данные отсутствуют!",
            "document_number": "Данные отсутствуют!",
            "document_style": "Данные отсутствуют!",
            "staff_division_name": "Данные отсутствуют!",
            "staff_division_nameKZ": "Данные отсутствуют!",
            "contractor_signer_name": {"name": "Неизвестный подписант"},
            "is_sgo": False,
        }
        for key, default_value in defaults.items():
            if values.get(key) is None:
                values[key] = default_value
        return values


# Модель для краткого представления emergency_contracts (для таймлайна)
class EmergencyContractReadShort(ReadModel):
    id: str = Field(default="00000000-0000-0000-0000-000000000000")
    date_from: datetime = Field(default_factory=lambda: datetime(1920, 1, 1))
    date_to: datetime = Field(default_factory=lambda: datetime(2500, 1, 1))
    created_at: datetime = Field(default_factory=lambda: datetime(1920, 1, 1))
    updated_at: datetime = Field(default_factory=lambda: datetime(1920, 1, 1))
    position_name: str = Field(default="Данные отсутствуют!")
    position_nameKZ: str = Field(default="Данные отсутствуют!")
    actual_position_name: str = Field(default="Данные отсутствуют!")
    actual_position_nameKZ: str = Field(default="Данные отсутствуют!")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        # Не забываем наследовать параметры из ReadModel, если нужно:
        allow_population_by_field_name = True
        exclude_unset = False
        json_encoders = {datetime: lambda v: v.isoformat()}

    @validator(
        "position_name", "position_nameKZ",
        "actual_position_name", "actual_position_nameKZ",
        pre=True, always=True
    )
    def default_empty_string(cls, v):
        return v if v is not None else "Данные отсутствуют!"

    @classmethod
    def from_orm(cls, orm_obj):
        position_name = orm_obj.position.name if getattr(orm_obj, "position", None) else "Данные отсутствуют!"
        position_nameKZ = orm_obj.position.nameKZ if getattr(orm_obj, "position", None) else "Данные отсутствуют!"
        actual_position_name = (orm_obj.actual_position.name
                                if getattr(orm_obj, "actual_position", None)
                                else "Данные отсутствуют!")
        actual_position_nameKZ = (orm_obj.actual_position.nameKZ
                                  if getattr(orm_obj, "actual_position", None)
                                  else "Данные отсутствуют!")
        return cls(
            id=orm_obj.id,
            date_from=orm_obj.date_from or datetime(1920, 1, 1),
            date_to=orm_obj.date_to or datetime(2500, 1, 1),
            created_at=orm_obj.created_at or datetime(1920, 1, 1),
            updated_at=orm_obj.updated_at or datetime(1920, 1, 1),
            position_name=position_name,
            position_nameKZ=position_nameKZ,
            actual_position_name=actual_position_name,
            actual_position_nameKZ=actual_position_nameKZ
        )


class ExperienceRead(ReadModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    document_number: Optional[str]
    name_of_organization: Optional[str]
    name_of_organizationKZ: Optional[str]
    is_credited: Optional[bool]
    document_style: Optional[str]
    date_credited: Optional[datetime]
    position_work_experience: Optional[str]
    position_work_experienceKZ: Optional[str]
    length_of_service: Optional[dict]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        date_to = orm_obj.date_to
        length_of_service = (
            get_date_difference(orm_obj.date_from, date_to)
            if orm_obj.is_credited else {"years": 99, "months": 12, "days": 1}
        )
        return cls(
            id=orm_obj.id,
            date_from=orm_obj.date_from,
            date_to=date_to,
            document_link=orm_obj.document_link,
            document_number=orm_obj.document_number,
            name_of_organization=orm_obj.name_of_organization,
            name_of_organizationKZ=orm_obj.name_of_organizationKZ,
            is_credited=orm_obj.is_credited if orm_obj.is_credited is not None else False,
            document_style=orm_obj.document_style,
            date_credited=orm_obj.date_credited,
            position_work_experience=orm_obj.position_work_experience,
            position_work_experienceKZ=orm_obj.position_work_experienceKZ,
            length_of_service=length_of_service,
        )


# Обновлённая схема ServiceIdInfoRead с корректными дефолтными значениями для enum-полей
class ServiceIdInfoRead(ReadModel):
    number: str
    token_number: str
    date_to: datetime
    token_status: str = Field(default="NOT_RECEIVED")
    id_status: str = Field(default="NOT_RECEIVED")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    # @root_validator(pre=True)
    # def fill_none_values(cls, values):
    #     values = dict(values)
    #     # Если в базе приходит значение, отличное от допустимых, заменяем его на "NOT_RECEIVED"
    #     if values.get("token_status") in [None, "Данные отсутствуют!"]:
    #         values["token_status"] = "NOT_RECEIVED"
    #     if values.get("id_status") in [None, "Данные отсутствуют!"]:
    #         values["id_status"] = "NOT_RECEIVED"
    #     if values.get("number") is None:
    #         values["number"] = "Данные отсутствуют!"
    #     if values.get("token_number") is None:
    #         values["token_number"] = "Данные отсутствуют!"
    #     if values.get("date_to") is None:
    #         values["date_to"] = datetime(1920, 1, 1)
    #     return values


class SecondmentRead(Model):
    id: str
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    staff_division: Optional[str]
    staff_divisionKZ: Optional[str]
    document_link: Optional[str]
    state_body: Optional[str]

    # @validator("staff_division", "staff_divisionKZ", "state_body", pre=True, always=True)
    # def default_empty_string(cls, v):
    #     return v if v is not None else "Данные отсутствуют!"
    #
    # @validator("document_link", pre=True, always=True)
    # def default_empty_link(cls, v):
    #     return v if v is not None else "https://example.com/default.pdf"

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        staff_division = orm_obj.secondment.name if orm_obj.secondment else "Данные отсутствуют!"
        staff_divisionKZ = orm_obj.secondment.nameKZ if orm_obj.secondment else "Данные отсутствуют!"
        body = orm_obj.secondment.state_body.name if orm_obj.secondment.state_body else "Данные отсутствуют!"
        return cls(
            id=orm_obj.id,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            staff_division=staff_division,
            staff_divisionKZ=staff_divisionKZ,
            document_link=orm_obj.document_link if orm_obj.document_link else "https://example.com/default.pdf",
            state_body=body
        )


class TypeOfArmyEquipmentModelRead(ReadNamedModel):
    type_of_equipment: Optional[dict]

    # @validator("type_of_equipment", pre=True, always=True)
    # def default_empty_dict(cls, v):
    #     return v if v is not None else {"name": "Неизвестно", "nameKZ": "Белгісіз"}

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            name=orm_obj.name,
            nameKZ=orm_obj.nameKZ,
            type_of_equipment={"name": orm_obj.type_of_army_equipment.name if orm_obj.type_of_army_equipment else "Неизвестно",
                               "nameKZ": orm_obj.type_of_army_equipment.nameKZ if orm_obj.type_of_army_equipment else "Белгісіз"}
        )


class TypeOfClothingEquipmentModelRead(ReadModel):
    type_of_equipment: Optional[dict]
    model_of_equipment: Optional[dict]

    # @validator("type_of_equipment", "model_of_equipment", pre=True, always=True)
    # def default_empty_dict(cls, v):
    #     return v if v is not None else {"name": "Неизвестно", "nameKZ": "Белгісіз"}

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            type_of_equipment={"name": orm_obj.type_cloth_equipmets.name if orm_obj.type_cloth_equipmets else "Неизвестно",
                               "nameKZ": orm_obj.type_cloth_equipmets.nameKZ if orm_obj.type_cloth_equipmets else "Белгісіз"},
            model_of_equipment={"name": orm_obj.type_cloth_eq_models.name if orm_obj.type_cloth_eq_models else "Неизвестно",
                                "nameKZ": orm_obj.type_cloth_eq_models.nameKZ if orm_obj.type_cloth_eq_models else "Белгісіз"}
        )


class TypeOfOtherEquipmentModelRead(ReadNamedModel):
    type_of_equipment: Optional[dict]

    # @validator("type_of_equipment", pre=True, always=True)
    # def default_empty_dict(cls, v):
    #     return v if v is not None else {"name": "Неизвестно", "nameKZ": "Белгісіз"}

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            name=orm_obj.name,
            nameKZ=orm_obj.nameKZ,
            type_of_equipment={"name": orm_obj.type_of_other_equipment.name if orm_obj.type_of_other_equipment else "Неизвестно",
                               "nameKZ": orm_obj.type_of_other_equipment.nameKZ if orm_obj.type_of_other_equipment else "Белгісіз"}
        )


class EquipmentRead(ReadModel):
    type_of_equipment: Optional[str]
    user_id: Optional[str]
    type_of_army_equipment_model_id: Optional[str]
    inventory_number: Optional[str]
    inventory_count: Optional[int]
    count_of_ammo: Optional[int]
    clothing_size: Optional[str]
    cloth_eq_types_models_id: Optional[str]
    type_of_other_equipment_model_id: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    type_of_army_equipment_model: Optional[TypeOfArmyEquipmentModelRead]
    cloth_eq_types_models: Optional[TypeOfClothingEquipmentModelRead]
    type_of_other_equipment_model: Optional[TypeOfOtherEquipmentModelRead]

    # @validator("type_of_equipment", "inventory_number", "clothing_size",
    #            "document_link", "document_number", pre=True, always=True)
    # def default_empty_string(cls, v):
    #     return v if v is not None else "Данные отсутствуют!"
    #
    # @validator("inventory_count", "count_of_ammo", pre=True, always=True)
    # def default_int(cls, v):
    #     return v if v is not None else 999999
    #
    # @validator("date_from", "date_to", pre=True, always=True)
    # def default_date(cls, v):
    #     return v if v is not None else datetime(1920, 1, 1, tzinfo=timezone.utc)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class HistoryTimelineDurationRead(Model):
    date_from: Optional[datetime]
    date_to: Optional[datetime]

    # @root_validator(pre=True)
    # def fill_default_dates(cls, values):
    #     values = dict(values)
    #     if values.get("date_from") is None:
    #         values["date_from"] = datetime(1920, 1, 1, tzinfo=timezone.utc)
    #     if values.get("date_to") is None:
    #         values["date_to"] = datetime(2500, 1, 1, tzinfo=timezone.utc)
    #     return values

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


# Схема для детального представления данных сервиса
class HistoryServiceDetailRead(Model):
    general_information: Optional[GeneralInformationRead]
    attendance: Optional[TrainingAttendanceRead]
    service_id_info: Optional[ServiceIdInfoRead]
    badges: Optional[List[BadgeServiceDetailRead]] = Field(default_factory=list)
    rank: Optional[RankRead]
    ranks: Optional[List[RankServiceDetailRead]]
    penalties: Optional[List[PenaltyRead]]
    contracts: Optional[List[ContractRead]]
    attestations: Union[Optional[List[AttestationRead]], str]
    characteristics: Union[Optional[List[CharacteristicRead]], str]
    holidays: Optional[List[HolidayRead]]
    emergency_contracts: List[EmergencyContractRead] = Field(default_factory=list)
    experience: Optional[List[ExperienceRead]]
    secondments: Optional[List[SecondmentRead]]
    equipments: Optional[List[EquipmentRead]]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


# Схема для таймлайна, где emergency_contracts представлены кратко
class HistoryTimeLineRead(Model):
    badges: Optional[List[HistoryTimelineDurationRead]]
    rank: Optional[RankRead]
    ranks: Optional[List[RankServiceDetailRead]]
    contracts: Optional[List[HistoryTimelineDurationRead]]
    emergency_contracts: Optional[List[EmergencyContractReadShort]]
    equipments: Optional[List[HistoryTimelineDurationRead]]
    academic_degrees: Optional[List[AcademicDegreeShorRead]]
    academic_titles: Optional[List[AcademicTitleShortRead]]
    educations: Optional[List[EducationShortRead]]
    courses: Optional[List[CourseShortRead]]
    driving_license: Optional[DrivingLicenseRead]
    identification_card: Optional[IdentificationCardRead]
    passport: Optional[PassportRead]

    # @validator('emergency_contracts', pre=True, each_item=True)
    # def ensure_dict(cls, value):
    #     # Если значение не dict, возвращаем словарь с дефолтными значениями
    #     if not isinstance(value, dict):
    #         return {
    #             "id": "00000000-0000-0000-0000-000000000000",
    #             "date_from": datetime(1920, 1, 1),
    #             "date_to": datetime(2500, 1, 1),
    #             "created_at": datetime(1920, 1, 1),
    #             "updated_at": datetime(1920, 1, 1),
    #             "position_name": "Данные отсутствуют!",
    #             "position_nameKZ": "Данные отсутствуют!",
    #             "actual_position_name": "Данные отсутствуют!",
    #             "actual_position_nameKZ": "Данные отсутствуют!"
    #         }
    #     return value

    class Config:
        arbitrary_types_allowed = True

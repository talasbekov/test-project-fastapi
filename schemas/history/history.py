import uuid
from enum import Enum
from decimal import Decimal
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from .general_information import GeneralInformationRead
from pydantic import BaseModel

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
    EducationShortRead
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

# Set time_zone to UTC(+06:00)
time_zone = timezone(timedelta(hours=6))


class StatusEnum(Enum):
    granted = "Присвоен"
    confirmed = "Подтвержден"
    canceled = "Отменен"


def get_date_difference(date1, date2):
    # Calculate the difference
    difference = date2 - date1

    # Extract years, months, and days from the difference
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


class HistoryBase(BaseModel):
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
    name_of_organizationKZ: Optional[str]
    type: str
    position_work_experience: Optional[str]
    position_work_experienceKZ: Optional[str]
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

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class HistoryCreate(HistoryBase):
    pass


class HistoryContractCreate(BaseModel):
    user_id: str
    type: str
    date_from: datetime
    date_to: Optional[datetime]
    document_number: str
    contract_type_id: str
    experience_years: Optional[int]
    date_credited: Optional[datetime]


class HistoryBadgeCreate(BaseModel):
    user_id: str
    type: str
    date_from: datetime
    date_to: Optional[datetime]
    document_number: str
    badge_type_id: str
    reason: str
    reasonKZ: str
    url: str


class HistorySecondmentCreate(BaseModel):
    user_id: str
    type: str
    date_from: datetime
    date_to: Optional[datetime]
    document_number: str
    staff_division_id: Optional[str]
    value: Optional[str]


class HistoryPenaltyCreate(BaseModel):
    user_id: str
    type: str
    date_from: datetime
    date_to: Optional[datetime]
    document_number: str
    penalty_type_id: str
    reason: str
    reasonKZ: str


class HistoryStatusCreate(BaseModel):
    user_id: str
    type: str
    date_from: datetime
    date_to: Optional[datetime]
    document_number: str
    status_type_id: str


class HistoryCoolnessCreate(BaseModel):
    user_id: str
    type: str
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_number: Optional[str]
    coolness_type_id: str
    coolness_status: str
    
class HistoryBlackBeretCreate(BaseModel):
    user_id: str
    type: str
    date_from: Optional[datetime]
    document_number: Optional[str]


class HistoryAttestationCreate(BaseModel):
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
        return get_status(self.coolness,
                          self.confirm_document_link,
                          self.cancel_document_link)

    @property
    def badge_status(self) -> Optional[dict]:
        return get_status(self.badge,
                          self.confirm_document_link,
                          self.cancel_document_link)

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
    penalty: Optional['PenaltyReadHistory']
    emergency_service: Optional['EmergencyServiceRead']
    work_experience: Optional['WorkExperienceRead']
    secondment: Optional['SecondmentReadHistory']
    name_change: Optional['NameChangeReadHistory']
    attestation: Optional['AttestationReadHistory']
    status: Optional['StatusReadHistory']
    coolness: Optional['CoolnessReadHistory']
    contract: Optional['ContractReadHistory']
    badge: Optional['BadgeReadHistory']
    document_link: Optional[str]
    confirm_document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: Optional[str]
    name_of_organization: Optional[str]
    user_id: str
    type: str
    coefficent: Optional[Decimal]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @property
    def service_characteristic(self) -> Optional[dict]:
        if self.characteristic_initiator is not None:
            return {"name": (self.characteristic_initiator.last_name
                             + ' '
                             + self.characteristic_initiator.first_name),
                    "nameKZ": (self.characteristic_initiator.last_name
                               + ' '
                               + self.characteristic_initiator.first_name)}
        else:
            return None

    @property
    def emergency_service(self) -> Optional[dict]:
        if self.coefficent is not None:
            return {"name": self.coefficent + " " + self.percentage,
                    "nameKZ": self.coefficent + " " + self.percentage}
        else:
            return None

    @property
    def work_experience(self) -> Optional[dict]:
        if self.name_of_organization is not None:
            return {"name": self.name_of_organization,
                    "nameKZ": self.name_of_organizationKZ}
        else:
            return None

    @property
    def coolness_status(self) -> Optional[dict]:
        return get_status(self.coolness,
                          self.confirm_document_link,
                          self.cancel_document_link)

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
        }

    @property
    def badge_status(self) -> Optional[dict]:
        if self.badge:
            status = 'Добавление'
            if self.cancel_document_link:
                status = 'Лишение'
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


class BadgeServiceDetailRead(ReadNamedModel):
    document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    url: Optional[str]
    reason: Optional[str]
    reasonKZ: Optional[str]

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

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            name=orm_obj.rank.name if orm_obj.rank else orm_obj.rank_name,
            nameKZ=orm_obj.rank.nameKZ if orm_obj.rank else orm_obj.rank_nameKZ,
            rank_id=orm_obj.rank.id if orm_obj.rank else None,
            document_link=orm_obj.document_link,
            rank_assigned_by=orm_obj.rank_assigned_by,
            document_number=orm_obj.document_number,
            document_style=orm_obj.document_style,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            early_promotion=orm_obj.early_promotion
        )


class PenaltyRead(Model):
    id: str
    status: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    cancel_document_link: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    reason: Optional[str]
    reasonKZ: Optional[str]
    penalty_id: Optional[str]

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
    contract_type_id: str
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: Optional[str]
    experience_years: Optional[int]
    date_credited: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
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
    attestation_statusKZ: Optional[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


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
        if crc_init:
            full_name = (f"{crc_init.last_name} {crc_init.first_name[0]}"
                         f".{'' if crc_init.father_name is None else crc_init.father_name[0]}")
        else:
            full_name = None
        return cls(
            id=orm_obj.id,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            document_link=orm_obj.document_link,
            cancel_document_link=orm_obj.cancel_document_link,
            document_number=orm_obj.document_number,
            characteristic_initiator=full_name,
            characteristic_initiator_id=orm_obj.characteristic_initiator_id,
        )


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
            document_link=orm_obj.document_link,
            cancel_document_link=orm_obj.cancel_document_link,
            document_number=orm_obj.document_number,
            status=orm_obj.status.type.name if orm_obj.status.type else orm_obj.status_name,
            status_type_id=orm_obj.status.type.id if orm_obj.status.type else None,
            status_id=orm_obj.status.id if orm_obj.status else None
        )


class EmergencyContactRead(ReadModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    length_of_service: Optional[dict]  # ВЫСЛУГА ЛЕТ
    coefficient: Optional[Decimal]  # КОЭФФИЦИЕНТ
    percentage: Optional[int]  # ПРОЦЕНТ
    staff_division: Optional[dict]
    position: Optional[dict]
    position_id: Optional[str]
    position_name: Optional[str]
    position_nameKZ: Optional[str]
    actual_position: Optional[dict]
    actual_position_id: Optional[str]
    actual_position_name: Optional[str]
    actual_position_nameKZ: Optional[str]
    emergency_rank_id: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    staff_division_id: Optional[str]
    document_style: Optional[str]
    contractor_signer_name: Optional[dict]
    date_credited: Optional[datetime]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        position_name = orm_obj.position.name if orm_obj.position else orm_obj.position_name
        position_nameKZ = orm_obj.position.nameKZ if orm_obj.position else orm_obj.position_nameKZ
        actual_position_name = (orm_obj.actual_position.name
                                if orm_obj.actual_position
                                else orm_obj.actual_position_name)
        actual_position_nameKZ = (orm_obj.actual_position.nameKZ
                                  if orm_obj.actual_position
                                  else orm_obj.actual_position_nameKZ)
        staff_division_name = (orm_obj.staff_division.name
                               if orm_obj.staff_division else orm_obj.staff_division_name)
        staff_division_nameKZ = (orm_obj.staff_division.nameKZ
                                 if orm_obj.staff_division else orm_obj.staff_division_nameKZ)

        date_to = orm_obj.date_to or datetime.now(orm_obj.date_from.tzinfo)
        length_of_service = get_date_difference(orm_obj.date_from, date_to)
        return cls(
            id=orm_obj.id,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            length_of_service=length_of_service,
            coefficient=orm_obj.coefficient,
            percentage=orm_obj.percentage,
            staff_division={"name": staff_division_name,
                            "nameKZ": staff_division_nameKZ},
            position={"name": position_name,
                      "nameKZ": position_nameKZ},
            position_id=orm_obj.position_id,
            actual_position={"name": actual_position_name,
                             "nameKZ": actual_position_nameKZ},
            actual_position_id=orm_obj.actual_position_id,
            document_link=orm_obj.document_link,
            document_number=orm_obj.document_number,
            staff_division_id=orm_obj.staff_division_id,
            document_style=orm_obj.document_style,
            contractor_signer_name={"name": orm_obj.contractor_signer_name,
                                    "nameKZ": orm_obj.contractor_signer_nameKZ},
            date_credited=orm_obj.date_credited
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
        date_to = orm_obj.date_to or datetime.now(orm_obj.date_from.tzinfo)
        if orm_obj.is_credited:
            length_of_service = get_date_difference(orm_obj.date_from, date_to)
        else:
            length_of_service = None
        return cls(
            id=orm_obj.id,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            document_link=orm_obj.document_link,
            document_number=orm_obj.document_number,
            name_of_organization=orm_obj.name_of_organization,
            name_of_organizationKZ=orm_obj.name_of_organizationKZ,
            is_credited=orm_obj.is_credited,
            document_style=orm_obj.document_style,
            date_credited=orm_obj.date_credited,
            position_work_experience=orm_obj.position_work_experience,
            position_work_experienceKZ=orm_obj.position_work_experienceKZ,
            length_of_service=length_of_service,
        )


class ServiceIdInfoRead(ReadModel):
    number: Optional[str]
    date_to: Optional[datetime]
    token_status: Optional[Enum]
    id_status: Optional[Enum]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class SecondmentRead(Model):
    id: str
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    staff_division: Optional[str]
    staff_divisionKZ: Optional[str]
    document_link: Optional[str]
    state_body: Optional[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        staff_division = (orm_obj.secondment.name
                          if orm_obj.secondment else None)
        staff_divisionKZ = (orm_obj.secondment.nameKZ
                            if orm_obj.secondment else None)

        body = (orm_obj.secondment.state_body.name
                if orm_obj.secondment.state_body else None)
        return cls(
            id=orm_obj.id,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            staff_division=staff_division,
            staff_divisionKZ=staff_divisionKZ,
            document_link=orm_obj.document_link,
            state_body=body
        )


class TypeOfArmyEquipmentModelRead(ReadNamedModel):
    type_of_equipment: Optional[dict]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            name=orm_obj.name,
            nameKZ=orm_obj.nameKZ,
            type_of_equipment={"name": orm_obj.type_of_army_equipment.name,
                               "nameKZ": orm_obj.type_of_army_equipment.nameKZ}
        )


class TypeOfClothingEquipmentModelRead(ReadModel):
    type_of_equipment: Optional[dict]
    model_of_equipment: Optional[dict]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            type_of_equipment={"name": orm_obj.type_cloth_equipmets.name,
                               "nameKZ": orm_obj.type_cloth_equipmets.nameKZ},
            model_of_equipment={"name": orm_obj.type_cloth_eq_models.name,
                                "nameKZ": orm_obj.type_cloth_eq_models.nameKZ}
        )


class TypeOfOtherEquipmentModelRead(ReadNamedModel):
    type_of_equipment: Optional[dict]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            name=orm_obj.name,
            nameKZ=orm_obj.nameKZ,
            type_of_equipment={"name": orm_obj.type_of_other_equipment.name,
                               "nameKZ": orm_obj.type_of_other_equipment.nameKZ}
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

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class HistoryServiceDetailRead(Model):
    general_information: Optional[GeneralInformationRead] = None
    attendance: Optional[TrainingAttendanceRead] = None
    service_id_info: Optional[ServiceIdInfoRead] = None
    badges: Optional[List[BadgeServiceDetailRead]] = None
    ranks: Optional[List[RankServiceDetailRead]] = None
    penalties: Optional[List[PenaltyRead]] = None
    contracts: Optional[List[ContractRead]] = None
    attestations: Optional[List[AttestationRead]] = None
    characteristics: Optional[List[CharacteristicRead]] = None
    holidays: Optional[List[HolidayRead]] = None
    emergency_contracts: Optional[List[EmergencyContactRead]] = None
    experience: Optional[List[ExperienceRead]] = None
    secondments: Optional[List[SecondmentRead]] = None
    equipments: Optional[List[EquipmentRead]] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class HistoryTimeLineRead(HistoryServiceDetailRead):
    academic_degrees: Optional[List[AcademicDegreeShorRead]]
    academic_titles: Optional[List[AcademicTitleShortRead]]
    educations: Optional[List[EducationShortRead]]
    courses: Optional[List[CourseShortRead]]
    driving_license: Optional[DrivingLicenseRead] = None
    identification_card: Optional[IdentificationCardRead] = None
    passport:  Optional[PassportRead] = None

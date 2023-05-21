import math
import uuid
from enum import Enum
from decimal import Decimal
from datetime import datetime
from typing import Optional, List, Union
from decimal import Decimal
import uuid
from .general_information import GeneralInformationRead
from schemas import PositionRead, RankRead
from enum import Enum
from pydantic import BaseModel

from schemas import (
    PositionRead,
    RankRead,
    UserRead,
    PenaltyRead,
    SecondmentRead,
    StatusRead,
    CoolnessRead,
    ContractRead,
    BadgeRead,
    StaffDivisionRead,
)
from schemas import Model, NamedModel, ReadModel, ReadNamedModel
from models import CoolnessStatusEnum

from .general_information import GeneralInformationRead
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
)

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
        dict_coolness = obj.dict()
        dict_coolness["status"] = status
        return dict_coolness
    else:
        return None

class HistoryBase(BaseModel):
    document_link: Optional[str]
    cancel_document_link: Optional[str]
    confirm_document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    position_id: Optional[uuid.UUID]
    rank_id: Optional[uuid.UUID]
    penalty_id: Optional[uuid.UUID]
    emergency_service_id: Optional[uuid.UUID]
    secondment_id: Optional[uuid.UUID]
    name_change_id: Optional[uuid.UUID]
    attestation_id: Optional[uuid.UUID]
    characteristic_initiator_id: Optional[uuid.UUID]
    rank_assigned_by: Optional[str]
    status_id: Optional[uuid.UUID]
    status_name: Optional[str]
    coolness_id: Optional[uuid.UUID]
    contract_id: Optional[uuid.UUID]
    badge_id: Optional[uuid.UUID]
    user_id: uuid.UUID
    is_credited: Optional[bool]
    document_style: Optional[str]
    date_credited: Optional[datetime]
    name_of_organization: Optional[str]
    type: str
    position_work_experience: Optional[str]
    staff_division_id: Optional[uuid.UUID]
    coefficient: Optional[Decimal]
    percentage: Optional[int]
    staff_division_name: Optional[str]
    staff_division_nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class HistoryCreate(HistoryBase):
    pass


class HistoryUpdate(HistoryBase):
    pass


class HistoryRead(HistoryBase, ReadNamedModel):
    rank: Optional[RankRead]
    position: Optional[PositionRead]
    penalty: Optional[PenaltyRead]
    secondment: Optional[SecondmentRead]
    status: Optional[StatusRead]
    coolness: Optional[CoolnessRead]
    contract: Optional[ContractRead]
    badge: Optional[BadgeRead]
    staff_division: Optional[StaffDivisionRead]

    class Config:
        orm_mode = True
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
            "position_work_experience": self.position_work_experience,
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
    rank: Optional['RankRead']
    penalty: Optional['PenaltyReadHistory']
    emergency_service: Optional['EmergencyServiceRead']
    work_experience: Optional['WorkExperienceRead']
    secondment: Optional['SecondmentReadHistory']
    name_change: Optional['NameChangeReadHistory']
    attestation: Optional['AttestationReadHistory']
    status: Optional['StatusReadHistory']
    coolness: Optional['CoolnessReadHistory']
    contract: Optional['ContractReadHistory']
    document_link: Optional[str]
    confirm_document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: Optional[str]
    name_of_organization: Optional[str]
    user_id: uuid.UUID
    type: str
    coefficent: Optional[Decimal]


    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


    @property
    def service_characteristic(self) -> Optional[dict]:
        if self.characteristic_initiator is not None:
            return {"name": self.characteristic_initiator.last_name + ' ' + self.characteristic_initiator.first_name,
                    "nameKZ": self.characteristic_initiator.last_name + ' ' + self.characteristic_initiator.first_name}
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
                    "nameKZ": self.name_of_organization}
        else:
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
            "document_link": self.document_link,
            "confirm_document_link": self.confirm_document_link,
            "cancel_document_link": self.cancel_document_link,
            "document_number": self.document_number,
            "user_id": self.user_id,
            "type": self.type,
            "service_characteristic": self.service_characteristic,
            "work_experience": self.work_experience,
        }

class AttendanceRead(Model):
    physical_training: Optional[int]
    tactical_training: Optional[int]
    shooting_training: Optional[int]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BadgeServiceDetailRead(ReadNamedModel):
    document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    url: Optional[str]

    class Config:
        orm_mode = True
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
            url=orm_obj.badge.type.url
        )

class RankServiceDetailRead(ReadNamedModel):
    rank_assigned_by: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_style: Optional[str]
    rank_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id= orm_obj.id,
            name=orm_obj.rank.name,
            nameKZ=orm_obj.rank.nameKZ,
            rank_id=orm_obj.rank.id,
            document_link=orm_obj.document_link,
            rank_assigned_by=orm_obj.rank_assigned_by,
            document_number=orm_obj.document_number,
            document_style=orm_obj.document_style,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
        )


class PenaltyRead(Model):
    status: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    cancel_document_link: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]

    """TODO: WHO IS THIS?"""

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            status=orm_obj.penalty.type.name,
            document_link=orm_obj.document_link,
            cancel_document_link=orm_obj.cancel_document_link,
            document_number=orm_obj.document_number,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
        )

class ContractRead(ReadNamedModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: Optional[str]
    experience_years: Optional[int]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            document_link=orm_obj.document_link,
            cancel_document_link=orm_obj.cancel_document_link,
            document_number=orm_obj.document_number,
            experience_years=orm_obj.experience_years,
            name=orm_obj.contract.type.name,
            nameKZ=orm_obj.contract.type.nameKZ,
        )


class AttestationRead(Model):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: Optional[str]
    attestation_status: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True




class CharacteristicRead(ReadModel):
    date_from : Optional[datetime]
    date_to : Optional[datetime]
    document_link : Optional[str]
    cancel_document_link: Optional[str]
    document_number : Optional[str]
    characteristic_initiator : Optional[str]
    characteristic_initiator_id : Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        crc_init = orm_obj.characteristic_initiator
        if crc_init:
            full_name = f"{crc_init.last_name} {crc_init.first_name[0]}.{crc_init.father_name[0]}."
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
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    cancel_document_link: Optional[str]
    document_number: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            document_link=orm_obj.document_link,
            cancel_document_link=orm_obj.cancel_document_link,
            document_number=orm_obj.document_number,
            status=orm_obj.status.type.name,
        )

class EmergencyContactRead(ReadModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    length_of_service: Optional[dict] # ВЫСЛУГА ЛЕТ
    coefficient: Optional[Decimal] # КОЭФФИЦИЕНТ
    percentage: Optional[int] # ПРОЦЕНТ
    staff_division: Optional[dict]
    position: Optional[dict]
    position_id: Optional[uuid.UUID]
    emergency_rank_id: Optional[uuid.UUID]
    document_link: Optional[str]
    document_number: Optional[str]
    staff_division_id: Optional[uuid.UUID]
    document_style: Optional[str]
    contractor_signer_name: Optional[dict]
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        position_name = orm_obj.position.name if orm_obj.position else None
        position_nameKZ = orm_obj.position.nameKZ if orm_obj.position else None
        staff_division_name = orm_obj.staff_division.name if orm_obj.staff_division else None
        staff_division_nameKZ = orm_obj.staff_division.nameKZ if orm_obj.staff_division else None

        date_to = orm_obj.date_to or datetime.now()
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
            document_link=orm_obj.document_link,
            document_number=orm_obj.document_number,
            staff_division_id=orm_obj.staff_division_id,
            document_style=orm_obj.document_style,
            contractor_signer_name={"name": orm_obj.contractor_signer_name,
                                    "nameKZ": orm_obj.contractor_signer_nameKZ}
        )


class ExperienceRead(ReadModel):
    date_from : Optional[datetime]
    date_to : Optional[datetime]
    document_link : Optional[str]
    document_number : Optional[str]
    name_of_organization : Optional[str]
    is_credited : Optional[bool]
    document_style : Optional[str]
    date_credited : Optional[datetime]
    position_work_experience : Optional[str]


    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            document_link=orm_obj.document_link,
            document_number=orm_obj.document_number,
            name_of_organization=orm_obj.name_of_organization,
            is_credited=orm_obj.is_credited,
            document_style=orm_obj.document_style,
            date_credited=orm_obj.date_credited,
            position_work_experience=orm_obj.position_work_experience,

        )


class ServiceIdInfoRead(ReadModel):
    number: Optional[str]
    date_to: Optional[datetime]
    token_status: Optional[Enum]
    id_status: Optional[Enum]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SecondmentRead(Model):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    staff_division: Optional[str]
    document_link: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            staff_division=orm_obj.secondment.staff_division.name,
            document_link=orm_obj.document_link,
        )

class TypeOfArmyEquipmentModelRead(ReadNamedModel):
    type_of_equipment: Optional[dict]

    class Config:
        orm_mode = True
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
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            type_of_equipment={"name": orm_obj.type_clothing_equipments.name,
                               "nameKZ": orm_obj.type_clothing_equipments.nameKZ},
            model_of_equipment={"name": orm_obj.type_clothing_equipment_models.name,
                                "nameKZ": orm_obj.type_clothing_equipment_models.nameKZ}
        )

class TypeOfOtherEquipmentModelRead(ReadNamedModel):
    type_of_equipment: Optional[dict]

    class Config:
        orm_mode = True
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
    user_id: Optional[uuid.UUID]
    type_of_army_equipment_model_id: Optional[uuid.UUID]
    inventory_number: Optional[str]
    inventory_count: Optional[int]
    count_of_ammo: Optional[int]
    clothing_size: Optional[str]
    clothing_equipment_types_models_id: Optional[uuid.UUID]
    type_of_other_equipment_model_id: Optional[uuid.UUID]
    document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    type_of_army_equipment_model: Optional[TypeOfArmyEquipmentModelRead]
    clothing_equipment_types_models: Optional[TypeOfClothingEquipmentModelRead]
    type_of_other_equipment_model: Optional[TypeOfOtherEquipmentModelRead]


    class Config:
        orm_mode = True
        arbitrary_types_allowed = True



class HistoryServiceDetailRead(Model):

    general_information: Optional[GeneralInformationRead]
    attendance: Optional[AttendanceRead]
    service_id_info: Optional[ServiceIdInfoRead]
    badges: Optional[List[BadgeServiceDetailRead]]
    ranks: Optional[List[RankServiceDetailRead]]
    penalties: Optional[List[PenaltyRead]]
    contracts: Optional[List[ContractRead]]
    attestations: Optional[List[AttestationRead]]
    characteristics: Optional[List[CharacteristicRead]]
    holidays: Optional[List[HolidayRead]]
    emergency_contracts: Optional[List[EmergencyContactRead]]
    experience: Optional[List[ExperienceRead]]
    secondments: Optional[List[SecondmentRead]]
    equipments: Optional[List[dict]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

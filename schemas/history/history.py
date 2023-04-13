from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Union
from decimal import Decimal
import uuid
from .general_information import GeneralInformationRead
from schemas import PositionRead, RankRead 
from enum import Enum

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
    BadgePersonalReadHistory
)

class HistoryBase(BaseModel):
    document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    position_id: Optional[uuid.UUID]
    rank_id: Optional[uuid.UUID]
    penalty_id: Optional[uuid.UUID]
    emergency_service_id: Optional[uuid.UUID]
    work_experience_id: Optional[uuid.UUID]
    secondment_id: Optional[uuid.UUID]
    name_change_id: Optional[uuid.UUID]
    attestation_id: Optional[uuid.UUID]
    service_characteristic_id: Optional[uuid.UUID]
    status_id: Optional[uuid.UUID]
    coolness_id: Optional[uuid.UUID]
    contract_id: Optional[uuid.UUID]
    characteristic_initiator_id: Optional[uuid.UUID]
    badge_id: Optional[uuid.UUID] 
    user_id: uuid.UUID
    type: str


    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class HistoryCreate(HistoryBase):
    pass


class HistoryUpdate(HistoryBase):
    pass


class HistoryRead(HistoryBase):
    id: uuid.UUID

class CharacteristicInitiator(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
 

class HistoryPersonalRead(BaseModel):
    id: uuid.UUID
    date_from: Optional[datetime]
    coefficient: Optional[Decimal]
    percentage: Optional[Decimal]
    characteristic_initiator_id: Optional[uuid.UUID]
    characteristic_initiator: Optional[CharacteristicInitiator]
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
    document_number: Optional[str]
    name_of_organization: Optional[str]
    user_id: uuid.UUID
    badge: Optional['BadgeServiceDetailRead']
    type: str
    badge: Optional['BadgePersonalReadHistory']


    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
 
    
    @property
    def emergency_service(self) -> Optional[dict]: 
        if self.coefficient is not None:
            return {"name": f"Коэффициент: {self.coefficient}, Процент: {self.percentage}%"}
        else:
            return None

    @property
    def work_experience(self) -> Optional[dict]:
        if self.name_of_organization is not None:
            return {"name" : self.name_of_organization}
        else:
            return None

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
            "coolness": self.coolness,
            "contract": self.contract,
            "document_link": self.document_link,
            "document_number": self.document_number, 
            "user_id": self.user_id,
            "type": self.type,
            "service_characteristic": self.service_characteristic,
            "work_experience": self.work_experience,
            "badge": self.badge,
        }

class AttendanceRead(BaseModel):
    physical_training: Optional[int]
    tactical_training: Optional[int]
    shooting_training: Optional[int]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BadgeServiceDetailRead(BaseModel):
    document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    name: Optional[str]
    url: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj): 
        return cls(
            document_link=orm_obj.document_link,
            document_number=orm_obj.document_number,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            name=orm_obj.badge.type.name,
            url=orm_obj.badge.type.url
        )

class RankServiceDetailRead(BaseModel):
    name: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.rank.name,
            document_link=orm_obj.document_link,
            document_number=orm_obj.document_number,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
        )

class PenaltyRead(BaseModel): 
    status: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
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
            document_number=orm_obj.document_number,
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
        )

class ContractRead(BaseModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    document_number: Optional[str]
    experience_years: Optional[int]
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            document_link=orm_obj.document_link,
            document_number=orm_obj.document_number,
            experience_years=orm_obj.experience_years,
            name=orm_obj.contract.type.name,
        )


class AttestationRead(BaseModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    document_number: Optional[str]
    attestation_status: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

     
class CharacteristicRead(BaseModel):
    id: uuid.UUID
    date_from : Optional[datetime]
    date_to : Optional[datetime]
    document_link : Optional[str]
    document_number : Optional[str]
    characteristic_initiator_id : Optional[uuid.UUID]
    characteristic_initiator : Optional[str]

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
            characteristic_initiator_id=orm_obj.characteristic_initiator_id,
            characteristic_initiator=orm_obj.characteristic_initiator.last_name + " " + orm_obj.characteristic_initiator.last_name[0] + "." + orm_obj.characteristic_initiator.father_name[0] + ".",
        )

class HolidayRead(BaseModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
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
            document_number=orm_obj.document_number,
            status=orm_obj.status.type.name,
        )

class EmergencyContactRead(BaseModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    length_of_service: Optional[int] # ВЫСЛУГА ЛЕТ
    coefficient: Optional[Decimal] # КОЭФФИЦИЕНТ  
    percentage: Optional[int] # ПРОЦЕНТ
    staff_division: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
    
    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            date_from=orm_obj.date_from,
            date_to=orm_obj.date_to,
            length_of_service=0,
            coefficient=orm_obj.coefficient,
            percentage=orm_obj.percentage,
            staff_division=orm_obj.staff_division.name,
        )
    

class ExperienceRead(BaseModel):
    date_from : Optional[datetime]
    date_to : Optional[datetime]
    document_link : Optional[str]
    document_number : Optional[str]
    name_of_organization : Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ServiceIdInfoRead(BaseModel):
    id: uuid.UUID
    number: Optional[str]
    date_to: Optional[datetime]
    token_status: Optional[Enum]
    id_status: Optional[Enum]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SecondmentRead(BaseModel):
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

class TypeOfArmyEquipmentModelRead(BaseModel):
    id: uuid.UUID
    name: Optional[str]
    type_of_equipment: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            name=orm_obj.name,
            type_of_equipment=orm_obj.type_of_army_equipment.name,
        )


class TypeOfClothingEquipmentModelRead(BaseModel):
    id: uuid.UUID
    name: Optional[str]
    type_of_equipment: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            name=orm_obj.name,
            type_of_equipment=orm_obj.type_of_clothing_equipment.name,
        )

class TypeOfOtherEquipmentModelRead(BaseModel):
    id: uuid.UUID
    name: Optional[str]
    type_of_equipment: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            name=orm_obj.name,
            type_of_equipment=orm_obj.type_of_other_equipment.name,
        )


class EquipmentRead(BaseModel):
    id: uuid.UUID
    type_of_equipment: Optional[str]
    user_id: Optional[uuid.UUID] 
    type_of_army_equipment_model_id: Optional[uuid.UUID]
    inventory_number: Optional[str]
    inventory_number_of_other_equipment: Optional[str]
    count_of_ammo: Optional[int] 
    type_of_clothing_equipment_model_id: Optional[uuid.UUID] 
    type_of_other_equipment_model_id: Optional[uuid.UUID]
    document_link: Optional[str]
    document_number: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    type_of_army_equipment_model: Optional[TypeOfArmyEquipmentModelRead]
    type_of_clothing_equipment_model: Optional[TypeOfClothingEquipmentModelRead]
    type_of_other_equipment_model: Optional[TypeOfOtherEquipmentModelRead]


    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

     
 
class HistoryServiceDetailRead(BaseModel):
 
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
    equipments: Optional[List[EquipmentRead]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

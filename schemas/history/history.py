from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Union
from decimal import Decimal
import uuid
from .general_information import GeneralInformationRead
from schemas import PositionRead, RankRead

from .history_personal import (
    PenaltyReadHistory,
    WorkExperienceRead,
    EmergencyServiceRead,
    AttestationReadHistory,
    NameChangeReadHistory,
    ServiceCharacteristicRead,
    StatusReadHistory,
    CoolnessReadHistory,
    SecondmentReadHistory,
    ContractReadHistory,
)


class HistoryBase(BaseModel):
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
    name: Optional[str]
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

 

class HistoryPersonalRead(BaseModel):
    id: uuid.UUID
    date_from: Optional[datetime]
    date_to: Optional[datetime] 
    position: Optional[PositionRead]
    rank: Optional['RankRead']
    penalty: Optional['PenaltyReadHistory']
    emergency_service: Optional['EmergencyServiceRead']
    work_experience: Optional['WorkExperienceRead']
    secondment: Optional['SecondmentReadHistory']
    name_change: Optional['NameChangeReadHistory']
    attestation: Optional['AttestationReadHistory']
    service_characteristic: Optional['ServiceCharacteristicRead']
    status: Optional['StatusReadHistory']
    coolness: Optional['CoolnessReadHistory']
    contract: Optional['ContractReadHistory']
    document_link: Optional[str]
    document_number: Optional[str]
    user_id: uuid.UUID
    type: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


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
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class RankServiceDetailRead(BaseModel):
    name: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PenaltyRead(BaseModel):
    name: Optional[str]
    status: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    """TODO: WHO IS THIS?"""

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ContractRead(BaseModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    document_number: Optional[str]
    number_of_years: Optional[int]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AttestationRead(BaseModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class CharacteristicRead(BaseModel):
    characteristic_from: Optional[str]
    document_link: Optional[str]
    date: Optional[datetime]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class HolidayRead(BaseModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    document_link: Optional[str]
    document_number: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class EmergencyContactRead(BaseModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    length_of_service: Optional[int] # ВЫСЛУГА ЛЕТ
    coefficient: Optional[int] # КОЭФФИЦИЕНТ
    name: Optional[str]
    percent: Optional[int] # ПРОЦЕНТ
    staff_division: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ExperienceRead(BaseModel):
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    name: Optional[str]
    description: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class ServiceIdInfoRead(BaseModel):
    number_token: Optional[str]
    number_service_id: Optional[str]
    end_date: Optional[datetime]
    status: Optional[str]

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

class EquipmentRead(BaseModel):
    name: Optional[str]
    type: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    inventory_number: Optional[int]
    date_start: Optional[datetime]
    count_of_ammo: Optional[int]

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
    emergency_contacts: Optional[List[EmergencyContactRead]]
    experience: Optional[List[ExperienceRead]]
    secondments: Optional[List[SecondmentRead]]
    equipments: Optional[List[EquipmentRead]]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

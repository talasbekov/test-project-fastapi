from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
import uuid


class PenaltyReadHistory(BaseModel):
    type: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            type=orm_obj.type.name,
        )


class WorkExperienceRead(BaseModel):
    num_of_organization: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class EmergencyServiceRead(BaseModel):
    coefficient: Optional[Decimal]
    percentage: Optional[int]
    staff_division: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AttestationReadHistory(BaseModel):
    status: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        print(orm_obj.attestation_history.attestation_status)
        return cls(
            status=orm_obj.attestation_history.attestation_status,
        )


class NameChangeReadHistory(BaseModel):
    name_before: Optional[str]
    name_after: Optional[str]
    name_type: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ServiceCharacteristicRead(BaseModel):
    characteristic_initiator: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            characteristic_initiator=orm_obj.characteristic_initiator,
        )


class StatusReadHistory(BaseModel):
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CoolnessReadHistory(BaseModel):
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.type.name,
        )


class ContractReadHistory(BaseModel):
    number_of_years: Optional[int]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SecondmentReadHistory(BaseModel):
    staff_division_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

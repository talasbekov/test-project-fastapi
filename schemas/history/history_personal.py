from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
import uuid


class PenaltyReadHistory(BaseModel):
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.type.name,
        )


class WorkExperienceRead(BaseModel):
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.num_of_organization,
        )

class EmergencyServiceRead(BaseModel):
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        coefficient = orm_obj.coefficient
        percentage = orm_obj.percentage
        staff_division = orm_obj.staff_division.name

        return cls(
            name=f"{staff_division} Департмент - ({coefficient}:{percentage}%)",
        )

class AttestationReadHistory(BaseModel):
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.attestation_history.attestation_status,
        )


class NameChangeReadHistory(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        name_before = orm_obj.name_before
        name_after = orm_obj.name_after
        name_type = orm_obj.name_type

        if name_type == 'name':
            name_type = 'Имя'
        elif name_type == 'surname':
            name_type = 'Фамилия'
        elif name_type == 'father_name':
            name_type = 'Отчество'
        name = f"{name_type}: {name_before} -> {name_after}"
        return cls(
            name=name,
        )

class BadgePersonalReadHistory(BaseModel):
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.type.name,
        )



class StatusReadHistory(BaseModel):
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.type.name,
        )


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
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):

        return cls(
            name=orm_obj.type.name,
        )

class SecondmentReadHistory(BaseModel):
    name: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.staff_division.name,
        )

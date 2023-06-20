from pydantic import BaseModel
from typing import Optional


class PenaltyReadHistory(BaseModel):
    name: Optional[str]
    nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.type.name,
            nameKZ=orm_obj.type.nameKZ,
        )


class WorkExperienceRead(BaseModel):
    name: Optional[str]
    nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.num_of_organization,
            nameKZ=orm_obj.num_of_organization,
        )


class EmergencyServiceRead(BaseModel):
    name: Optional[str]
    nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        coefficient = orm_obj.coefficient
        percentage = orm_obj.percentage
        staff_division = orm_obj.staff_division.name
        staff_divisionKZ = orm_obj.staff_division.nameKZ
        return cls(
            name=f"{staff_division} Департмент - ({coefficient}:{percentage}%)",
            nameKZ=f"{staff_divisionKZ} Департмент - ({coefficient}:{percentage}%)",
        )


class AttestationReadHistory(BaseModel):
    name: Optional[str]
    nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.attestation_history.attestation_status,
            nameKZ=orm_obj.attestation_history.attestation_status,
        )


class NameChangeReadHistory(BaseModel):
    name: str
    nameKZ: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        name_before = orm_obj.name_before
        name_after = orm_obj.name_after
        name_type = orm_obj.name_type
        name_typeKZ = orm_obj.name_type

        if name_type == 'name':
            name_type = 'Имя'
            name_typeKZ = 'Аты'
        elif name_type == 'surname':
            name_type = 'Фамилия'
            name_typeKZ = 'Тегі'
        elif name_type == 'father_name':
            name_type = 'Отчество'
            name_typeKZ = 'Әкесінің аты'
        name = f"{name_type}: {name_before} -> {name_after}"
        nameKZ = f"{name_typeKZ}: {name_before} -> {name_after}"
        return cls(
            name=name,
            nameKZ=nameKZ,
        )


class BadgePersonalReadHistory(BaseModel):
    name: Optional[str]
    nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.type.name,
            nameKZ=orm_obj.type.nameKZ,
        )


class StatusReadHistory(BaseModel):
    name: Optional[str]
    nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.type.name,
            nameKZ=orm_obj.type.nameKZ,
        )


class CoolnessReadHistory(BaseModel):
    name: Optional[str]
    nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.type.name,
            nameKZ=orm_obj.type.nameKZ,
        )


class ContractReadHistory(BaseModel):
    name: Optional[str]
    nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):

        return cls(
            name=orm_obj.type.name,
            nameKZ=orm_obj.type.nameKZ,
        )


class BadgeReadHistory(BaseModel):
    name: Optional[str]
    nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):

        return cls(
            name=orm_obj.type.name,
            nameKZ=orm_obj.type.nameKZ,
        )

class SecondmentReadHistory(BaseModel):
    name: Optional[str]
    nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            name=orm_obj.staff_division.name,
            nameKZ=orm_obj.staff_division.nameKZ,
        )

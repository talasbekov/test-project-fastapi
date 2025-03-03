from typing import Optional
from schemas import CustomBaseModel


class PenaltyReadHistory(CustomBaseModel):
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


class WorkExperienceRead(CustomBaseModel):
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


class EmergencyServiceRead(CustomBaseModel):
    name: Optional[str] = "Данные отсутствуют"
    nameKZ: Optional[str] = "Данные отсутствуют"

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


class AttestationReadHistory(CustomBaseModel):
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


class NameChangeReadHistory(CustomBaseModel):
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


class BadgePersonalReadHistory(CustomBaseModel):
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


class StatusReadHistory(CustomBaseModel):
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


class CoolnessReadHistory(CustomBaseModel):
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


class ContractReadHistory(CustomBaseModel):
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


class BadgeReadHistory(CustomBaseModel):
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

class SecondmentReadHistory(CustomBaseModel):
    name: Optional[str]
    nameKZ: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def from_orm(cls, orm_obj):
        division_name = getattr(orm_obj.staff_division, 'name', None)
        division_nameKZ = getattr(orm_obj.staff_division, 'nameKZ', None)
        if division_name:
            return cls(
                name=orm_obj.name + ": " + division_name,
                nameKZ=orm_obj.nameKZ + ": " + division_nameKZ,
            )
        return cls(
            name=orm_obj.name,
            nameKZ=orm_obj.nameKZ,
        )

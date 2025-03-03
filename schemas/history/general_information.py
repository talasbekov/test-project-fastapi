import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, root_validator

from schemas import ReadModel
from schemas import PrivelegeEmergencyRead, PersonnalReserveRead, CoolnessRead, RecommenderUserRead
from schemas.base import CustomBaseModel


def default_string(value: Optional[str]) -> str:
    return value if value is not None else "Данные отсутствуют!"


def default_date(value: Optional[datetime]) -> datetime:
    return value if value is not None else datetime(1920, 1, 1)


class OathRead(ReadModel):
    date: Optional[datetime]
    military_id: Optional[str]
    military_name: Optional[str]
    military_nameKZ: Optional[str]

    @root_validator(pre=True)
    def fill_defaults(cls, values):
        values = dict(values)
        values["date"] = default_date(values.get("date"))
        values["military_id"] = default_string(values.get("military_id"))
        values["military_name"] = default_string(values.get("military_name"))
        values["military_nameKZ"] = default_string(values.get("military_nameKZ"))
        return values

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            date=orm_obj.date,
            military_id=orm_obj.military_unit_id,
            military_name=(
                orm_obj.military_unit.name
                if getattr(orm_obj, "military_unit", None) and orm_obj.military_unit.name
                else "Данные отсутствуют!"
            ),
            military_nameKZ=getattr(orm_obj.military_unit, "nameKZ", "Данные отсутствуют!")
        )


class BlackBeretRead(CustomBaseModel):
    id: Optional[str]
    badge_id: Optional[str]
    date_from: Optional[datetime]
    document_number: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    @root_validator(pre=True)
    def fill_defaults(cls, values):
        values = dict(values)
        values["id"] = values.get("id") or str(uuid.uuid4())
        values["badge_id"] = values.get("badge_id") or str(uuid.uuid4())
        values["date_from"] = default_date(values.get("date_from"))
        values["document_number"] = default_string(values.get("document_number"))
        return values


class GeneralInformationRead(CustomBaseModel):
    oath: Optional[OathRead]
    privilege_emergency_secrets: Optional[PrivelegeEmergencyRead]
    personnel_reserve: Optional[PersonnalReserveRead] = Field(alias='personnel_reserve', default_factory=dict)
    coolness: Optional[List[CoolnessRead]]
    black_beret: Optional[BlackBeretRead]
    recommender: Optional[RecommenderUserRead] = Field(alias='recommender', default_factory=dict)

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

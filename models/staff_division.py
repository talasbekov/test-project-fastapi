import enum
import json

from sqlalchemy import Column, ForeignKey, Boolean, Integer, String
from sqlalchemy.dialects.oracle import CLOB
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for

from models import NamedNestedModel, isActiveModel


class StaffDivisionEnum(str, enum.Enum):
    SPECIAL_GROUP = "Особая группа"
    CANDIDATES = "Кандидаты"
    DEAD = "Умер"
    RETIRED = "В отставке"
    IN_RESERVE = "В запасе"
    REMOVED_FROM_LIST = "Исключен из списков личного состава"
    SECONDMENT_OTHER = "Откомандирован в другой орган"
    PERISHED = "Погиб"
    SERVICE = 'СГО РК'
    DISPOSITION = 'В распоряжении'
    OUT_STAFF = 'Внештатный сотрудник'


class StaffDivision(NamedNestedModel, isActiveModel):

    __tablename__ = "hr_erp_staff_divisions"

    # Properties
    parent_group_id = Column(String(), ForeignKey(
        "hr_erp_staff_divisions.id"), nullable=True)
    description = Column(CLOB)
    is_combat_unit = Column(Boolean)
    leader_id = Column(String(), ForeignKey(
        "hr_erp_staff_units.id"), nullable=True)
    staff_division_number = Column(Integer)
    type_id = Column(String(), ForeignKey("hr_erp_staff_division_types.id"))
    type = relationship("StaffDivisionType")
    # Relationships
    children = relationship("StaffDivision")
    staff_units = relationship("StaffUnit",
                               back_populates="staff_division",
                               cascade="all,delete",
                               foreign_keys="StaffUnit.staff_division_id")
    leader = relationship("StaffUnit", foreign_keys=leader_id)
    curators = relationship(
        "StaffUnitDivisions", back_populates="staff_division", foreign_keys="StaffUnitDivisions.curator_of_id")
    # curators = relationship("StaffUnitDivision", back_populates="staff_division")

@listens_for(StaffDivision, 'before_update')
def description_set_listener(mapper, connection, target):
    if isinstance(target.description, dict):
        target.description = json.dumps(target.description)
        
@listens_for(StaffDivision, 'before_insert')
def description_set_listener(mapper, connection, target):
    if isinstance(target.description, dict):
        target.description = json.dumps(target.description)

import enum

from sqlalchemy import Column, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.orm import relationship

from models import NamedNestedModel, isActiveModel


class StaffDivisionEnum(str, enum.Enum):
    SPECIAL_GROUP = "Особая группа"
    CANDIDATES = "Кандидаты"
    DEAD = "Умер"
    RETIRED = "В отставке"
    IN_RESERVE = "В запасе"
    REMOVED_FROM_LIST = "Исключен из списков личного состава"
    SECONDMENT_OTHER = "Откомандирован в другой гос. орган"
    PERISHED = "Погиб"


class StaffDivision(NamedNestedModel, isActiveModel):

    __tablename__ = "staff_divisions"

    parent_group_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)
    description = Column(TEXT)
    is_combat_unit = Column(Boolean)
    leader_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"), nullable=True)

    children = relationship("StaffDivision")

    staff_units = relationship("StaffUnit", back_populates="staff_division", cascade="all,delete", foreign_keys="StaffUnit.staff_division_id")

    leader = relationship("StaffUnit", foreign_keys=leader_id)

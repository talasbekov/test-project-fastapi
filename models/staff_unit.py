import uuid

from sqlalchemy import TEXT, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model

from .association import staff_unit_function


class StaffUnit(Model, Base):

    __tablename__ = "staff_units"

    position_id = Column(UUID(as_uuid=True), nullable=False)
    staff_division_id = Column(UUID(as_uuid=True), nullable=False)

    user = relationship("User")
    staff_functions = relationship("StaffFunction",
                                   secondary=staff_unit_function)
    position = relationship("Position", cascade="all,delete")
    staff_division = relationship("StaffDivision", cascade="all,delete")

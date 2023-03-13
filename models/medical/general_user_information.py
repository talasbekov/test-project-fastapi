import uuid

from sqlalchemy import Column, Enum as EnumType, ForeignKey, Integer, String, text, Double
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship
from enum import Enum

from core import Base
from models import Model


class BloodType(str, Enum):
    O_PLUS = "O (I) Rh+"
    O_MINUS = "O (I) Rh-"
    A_PLUS = "A (II) Rh+"
    A_MINUS = "A (II) Rh-"
    B_PLUS = "B (III) Rh+"
    B_MINUS = "B (III) Rh-"
    AB_PLUS = "AB (IV) Rh+"
    AB_MINUS = "AB (IV) Rh-"


class GeneralUserInformation(Model):

    __tablename__ = "general_user_informations"

    height = Column(Integer)
    blood_group = Column(EnumType(BloodType), nullable=True, default=BloodType.O_PLUS)
    age_group_id = Column(UUID(as_uuid=True), ForeignKey("age_groups.id"))
    profile_id = Column(UUID(as_uuid=True), ForeignKey("medical_profiles.id"))
    weight = Column(Integer)

    profile = relationship("MedicalProfile")

import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class BloodType(str,Enum):
    O_PLUS = "0+"
    O_MINUS = "0-"
    A_PLUS = "A+"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B_MINUS = "B-"
    AB_PLUS = "AB+"
    AB_MINUS = "AB-"


class AgeGroup(int,Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6


class GeneralUserInformation(Model):

    __tablename__ = "general_user_informations"

    height = Column(Integer)
    blood_group = Column(BloodType)
    age_group = Column(AgeGroup)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("medical_profiles.id"))

    profile = relationship("MedicalProfile")

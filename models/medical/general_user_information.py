from enum import Enum

from sqlalchemy import Column, Enum as EnumType, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

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


class AgeGroup(int, Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6


class GeneralUserInformation(Model):

    __tablename__ = "general_user_informations"

    height = Column(Integer)
    blood_group = Column(
        EnumType(BloodType),
        nullable=True,
        default=BloodType.O_PLUS)
    age_group = Column(
        EnumType(AgeGroup),
        nullable=True,
        default=AgeGroup.FIRST)
    profile_id = Column(String(), ForeignKey("medical_profiles.id"))
    weight = Column(Integer)

    profile = relationship("MedicalProfile")

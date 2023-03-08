import uuid

from sqlalchemy import BigInteger, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class MedicalProfile(Model):

    __tablename__ = "medical_profiles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"))

    profile = relationship("Profile", back_populates="medical_profile")

    hospital_datas = relationship("HospitalData", back_populates="profile")
    dispensary_registrations = relationship("DispensaryRegistration", back_populates="profile")
    user_liberations = relationship("UserLiberation", back_populates="profile")
    anthropometric_datas = relationship("AnthropometricData", back_populates="profile")
    general_user_informations = relationship("GeneralUserInformation", back_populates="profile")
    
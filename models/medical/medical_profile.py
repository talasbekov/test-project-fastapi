from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class MedicalProfile(Model):

    __tablename__ = "medical_profiles"

    profile_id = Column(String(), ForeignKey("profiles.id"))

    profile = relationship("Profile", back_populates="medical_profile")

    hospital_datas = relationship("HospitalData", back_populates="profile")
    dispensary_registrations = relationship(
        "DispensaryRegistration", back_populates="profile")
    user_liberations = relationship("UserLiberation", back_populates="profile")
    anthropometric_datas = relationship(
        "AnthropometricData", back_populates="profile")
    general_user_informations = relationship(
        "GeneralUserInformation", back_populates="profile")

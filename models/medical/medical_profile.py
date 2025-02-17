from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.medical import DispensaryRegistration
from .user_liberation import UserLiberation
from models import Model


class MedicalProfile(Model):

    __tablename__ = "hr_erp_medical_profiles"

    profile_id = Column(String(), ForeignKey("hr_erp_profiles.id"))

    profile = relationship("Profile", back_populates="medical_profile")

    dispensary_registrations = relationship("DispensaryRegistration", back_populates="profile", foreign_keys=[DispensaryRegistration.medical_profile_id])
    hospital_datas = relationship("HospitalData", back_populates="profile")
    user_liberations = relationship("UserLiberation", back_populates="profile", foreign_keys=[UserLiberation.medical_profile_id])
    anthropometric_datas = relationship("AnthropometricData", back_populates="profile")
    general_user_info = relationship("GeneralUserInformation", back_populates="profile")

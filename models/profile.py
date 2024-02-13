from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class Profile(Model):

    __tablename__ = "hr_erp_profiles"

    user_id = Column(
        String(),
        ForeignKey("hr_erp_users.id"),
        nullable=False)
    user = relationship("User", back_populates="profile")

    educational_profile = relationship(
        "EducationalProfile",
        back_populates="profile",
        cascade="all,delete",
        uselist=False)
    additional_profile = relationship(
        "AdditionalProfile",
        cascade="all, delete",
        back_populates="profile",
        uselist=False)
    personal_profile = relationship(
        "PersonalProfile",
        back_populates="profile",
        cascade="all,delete",
        uselist=False)
    medical_profile = relationship(
        "MedicalProfile",
        back_populates="profile",
        cascade="all,delete",
        uselist=False)
    family_profile = relationship(
        "FamilyProfile",
        back_populates="profile",
        cascade="all,delete",
        uselist=False)

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class Profile(Model):

    __tablename__ = "profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="profile")

    educational_profile = relationship("EducationalProfile", back_populates="profile", cascade="all,delete", uselist=False)
    additional_profile = relationship("AdditionalProfile", cascade="all, delete", back_populates="profile", uselist=False)
    personal_profile = relationship("PersonalProfile", back_populates="profile", cascade="all,delete", uselist=False)
    medical_profile = relationship("MedicalProfile", back_populates="profile", cascade="all,delete", uselist=False)
    family_profile = relationship("FamilyProfile", back_populates="profile", cascade="all,delete", uselist=False)

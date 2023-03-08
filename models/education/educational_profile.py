from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class EducationalProfile(Model, Base):

    __tablename__ = "educational_profiles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    profile = relationship("Profile", back_populates="educational_profile")

    academic_degree = relationship("AcademicDegree", back_populates="profile", cascade="all, delete")
    academic_title = relationship("AcademicTitle", back_populates="profile", cascade="all, delete")
    education = relationship("Education", back_populates="profile", cascade="all, delete")
    course = relationship("Course", back_populates="profile", cascade="all, delete")
    language_proficiency = relationship("LanguageProficiency", back_populates="profile", cascade="all, delete")

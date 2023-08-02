from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class EducationalProfile(Model):

    __tablename__ = "educational_profiles"

    profile_id = Column(String(), ForeignKey(
        "profiles.id"), nullable=True)
    profile = relationship("Profile", back_populates="educational_profile")

    academic_degree = relationship(
        "AcademicDegree", back_populates="profile", cascade="all, delete")
    academic_title = relationship(
        "AcademicTitle", back_populates="profile", cascade="all, delete")
    education = relationship(
        "Education", back_populates="profile", cascade="all, delete")
    course = relationship(
        "Course", back_populates="profile", cascade="all, delete")
    language_proficiency = relationship(
        "LanguageProficiency",
        back_populates="profile",
        cascade="all, delete",
        lazy="joined")

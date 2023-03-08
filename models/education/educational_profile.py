from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class EducationalProfile(Model, Base):

    __tablename__ = "educational_profiles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    profile = relationship("Profile", back_populates="educational_profile")

    academic_degree = relationship("AcademicDegree")
    academic_title = relationship("AcademicTitle")
    education = relationship("Education")
    course = relationship("Course")
    language_proficiency = relationship("LanguageProficiency")

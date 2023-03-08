from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import DATE, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class AcademicTitle(Model, Base):

    __tablename__ = "academic_titles"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("educational_profiles.id"), nullable=True)
    profile = relationship("EducationalProfile", back_populates="academic_title")

    degree_id = Column(UUID(as_uuid=True), ForeignKey("academic_title_degrees.id"), nullable=True)
    degree = relationship("AcademicTitleDegree")

    specialty_id = Column(UUID(as_uuid=True), ForeignKey("specialties.id"), nullable=True)
    specialty = relationship("Specialty")

    document_number = Column(String)
    document_link = Column(String)
    assignment_date = Column(DATE)

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import DATE, TEXT
from sqlalchemy.orm import relationship

from models import Model


class AcademicTitle(Model):

    __tablename__ = "hr_erp_academic_titles"

    educational_profile_id = Column(String(), ForeignKey(
        "hr_erp_educational_profiles.id"), nullable=True)
    profile_id = Column(String(), nullable=True)
    profile = relationship(
        "EducationalProfile",
        back_populates="academic_title")

    degree_id = Column(String(), ForeignKey(
        "hr_erp_academic_title_degrees.id"), nullable=True)
    degree = relationship(
        "AcademicTitleDegree",
        back_populates="academic_title")

    specialty_id = Column(
        String(),
        ForeignKey("hr_erp_specialties.id"),
        nullable=True)
    specialty = relationship("Specialty", back_populates="academic_title")

    document_number = Column(String)
    document_link = Column(TEXT, nullable=True)
    assignment_date = Column(DATE)

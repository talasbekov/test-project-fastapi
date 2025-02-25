from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import DATE, TEXT
from sqlalchemy.orm import relationship

from models import Model


class AcademicDegree(Model):

    __tablename__ = "hr_erp_academic_degrees"

    educational_profile_id = Column(String(), ForeignKey(
        "hr_erp_educational_profiles.id"), nullable=True)
    profile_id = Column(String(), nullable = True)
    profile = relationship(
        "EducationalProfile",
        back_populates="academic_degree")

    degree_id = Column(String(), ForeignKey(
        "dic_hr_erp_academic_degree_degrees.id"), nullable=True)
    degree = relationship(
        "AcademicDegreeDegree",
        back_populates="academic_degree")

    science_id = Column(
        String(),
        ForeignKey("hr_erp_sciences.id"),
        nullable=True)
    science = relationship("Science", back_populates="academic_degree")

    specialty_id = Column(
        String(),
        ForeignKey("hr_erp_specialties.id"),
        nullable=True)
    specialty = relationship("Specialty", back_populates="academic_degree")

    document_number = Column(String)
    document_link = Column(TEXT, nullable=True)
    assignment_date = Column(DATE)

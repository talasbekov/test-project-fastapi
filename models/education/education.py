from sqlalchemy import Column, ForeignKey, Boolean, String
from sqlalchemy.dialects.postgresql import DATE, TEXT
from sqlalchemy.orm import relationship

from models import Model


class Education(Model):

    __tablename__ = "educations"

    profile_id = Column(String(), ForeignKey(
        "educational_profiles.id"), nullable=True)
    profile = relationship("EducationalProfile", back_populates="education")
    is_military_school = Column(Boolean, nullable=True, default=False)

    specialty_id = Column(
        String(),
        ForeignKey("specialties.id"),
        nullable=True)
    specialty = relationship("Specialty", back_populates="education")

    type_of_top = Column(TEXT)
    document_number = Column(TEXT)
    date_of_issue = Column(DATE)

    start_date = Column(DATE)
    end_date = Column(DATE)

    institution_id = Column(
        String(),
        ForeignKey("institutions.id"),
        nullable=True)
    institution = relationship("Institution", back_populates="education")

    degree_id = Column(String(),
                       ForeignKey("institution_degree_types.id"))
    degree = relationship(
        "InstitutionDegreeType",
        back_populates="education",
        foreign_keys=degree_id)

    document_link = Column(TEXT, nullable=True)

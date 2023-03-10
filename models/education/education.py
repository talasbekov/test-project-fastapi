from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, DATE, TEXT

from models import Model


class Education(Model):

    __tablename__ = "educations"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("educational_profiles.id"), nullable=True)
    profile = relationship("EducationalProfile", back_populates="education")

    start_date = Column(DATE)
    end_date = Column(DATE)

    institution_id = Column(UUID(as_uuid=True), ForeignKey("institutions.id"), nullable=True)
    institution = relationship("Institution", back_populates="education")

    degree_id = Column(UUID(as_uuid=True), ForeignKey("institution_degree_types.id"))
    degree = relationship("InstitutionDegreeType", back_populates="education", foreign_keys=degree_id)

    document_link = Column(TEXT)

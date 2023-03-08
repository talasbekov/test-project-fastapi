from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, DATE

from core import Base
from models import Model


class Education(Model, Base):

    __tablename__ = "educations"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("educational_profiles.id"), nullable=True)
    profile = relationship("EducationalProfile", back_populates="education")

    start_date = Column(DATE)
    end_date = Column(DATE)

    institution_id = Column(UUID(as_uuid=True), ForeignKey("institutions.id"), nullable=True)
    institution = relationship("Institution")

    degree_id = Column(String)
    document_link = Column(String)

    institution_degree_type = relationship("InstitutionDegreeType")

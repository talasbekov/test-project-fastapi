from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import DATE, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class AcademicDegree(Model, Base):

    __tablename__ = "academic_degrees"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("educational_profiles.id"), nullable=True)
    profile = relationship("EducationalProfile")

    degree_id = Column(UUID(as_uuid=True), ForeignKey("academic_degree_degrees.id"), nullable=True)
    degree = relationship("AcademicDegreeDegree")

    science_id = Column(UUID(as_uuid=True), ForeignKey("sciences.id"), nullable=True)
    science = relationship("Science")

    document_number = Column(String)
    document_link = Column(String)
    assignment_date = Column(DATE)

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import DATE, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class Course(Model, Base):

    __tablename__ = "courses"

    name = Column(String)

    profile_id = Column(UUID(as_uuid=True), ForeignKey("educational_profiles.id"), nullable=True)
    profile = relationship("EducationalProfile")

    provider_id = Column(String)

    course_provider_id = Column(UUID(as_uuid=True), ForeignKey("course_providers.id"), nullable=True)
    course_provider = relationship("CourseProvider")

    start_date = Column(DATE)
    end_date = Column(DATE)
    document_link = Column(String)

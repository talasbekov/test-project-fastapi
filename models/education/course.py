from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import DATE, UUID, TEXT
from sqlalchemy.orm import relationship

from models import NamedModel


class Course(NamedModel):

    __tablename__ = "courses"

    profile_id = Column(UUID(as_uuid=True), ForeignKey(
        "educational_profiles.id"), nullable=True)
    profile = relationship("EducationalProfile", back_populates="course")

    course_provider_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey("course_providers.id"),
        nullable=True)
    course_provider = relationship("CourseProvider", back_populates="course")

    start_date = Column(DATE)
    end_date = Column(DATE)
    document_link = Column(TEXT, nullable=True)

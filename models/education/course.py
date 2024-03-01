from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import DATE, TEXT
from sqlalchemy.orm import relationship

from models import NamedModel


class Course(NamedModel):

    __tablename__ = "hr_erp_courses"

    profile_id = Column(String(), ForeignKey(
        "hr_erp_educational_profiles.id"), nullable=True)
    profile = relationship("EducationalProfile", back_populates="course")

    course_provider_id = Column(
        String(),
        ForeignKey("hr_erp_course_providers.id"),
        nullable=True)
    course_provider = relationship("CourseProvider", back_populates="course")

    start_date = Column(DATE)
    end_date = Column(DATE)
    document_link = Column(TEXT, nullable=True)

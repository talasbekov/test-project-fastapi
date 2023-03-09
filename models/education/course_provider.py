from sqlalchemy.orm import relationship

from models import NamedModel


class CourseProvider(NamedModel):

    __tablename__ = "course_providers"

    course = relationship("Course", back_populates="course_provider")

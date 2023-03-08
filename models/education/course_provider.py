from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core import Base
from models import NamedModel


class CourseProvider(NamedModel):

    __tablename__ = "course_providers"

    course = relationship("Course", back_populates="course_provider")

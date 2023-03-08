from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class CourseProvider(Model, Base):

    __tablename__ = "course_providers"

    name = Column(String)

    course = relationship("Course")

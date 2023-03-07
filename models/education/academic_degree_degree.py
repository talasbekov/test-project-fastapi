from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class AcademicDegreeDegree(Model, Base):

    __tablename__ = "academic_degree_degrees"

    name = Column(String)

    academic_degree = relationship("AcademicDegree")

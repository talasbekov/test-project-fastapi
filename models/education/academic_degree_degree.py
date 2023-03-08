from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core import Base
from models import NamedModel


class AcademicDegreeDegree(NamedModel):

    __tablename__ = "academic_degree_degrees"

    academic_degree = relationship("AcademicDegree", back_populates="degree")

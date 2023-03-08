from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core import Base
from models import NamedModel


class Science(NamedModel):

    __tablename__ = "sciences"

    academic_degree = relationship("AcademicDegree", back_populates="science")

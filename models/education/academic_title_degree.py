from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core import Base
from models import NamedModel


class AcademicTitleDegree(NamedModel):

    __tablename__ = "academic_title_degrees"

    academic_title = relationship("AcademicTitle", back_populates="degree")

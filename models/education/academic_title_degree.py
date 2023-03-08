from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class AcademicTitleDegree(Model, Base):

    __tablename__ = "academic_title_degrees"

    name = Column(String)

    academic_title = relationship("AcademicTitle")

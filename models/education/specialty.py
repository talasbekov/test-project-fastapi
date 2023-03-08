from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core import Base
from models import Model


class Specialty(Model, Base):

    __tablename__ = "specialties"

    name = Column(String)

    academic_title = relationship("AcademicTitle")

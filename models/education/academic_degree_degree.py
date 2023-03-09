from sqlalchemy.orm import relationship

from models import NamedModel


class AcademicDegreeDegree(NamedModel):

    __tablename__ = "academic_degree_degrees"

    academic_degree = relationship("AcademicDegree", back_populates="degree")

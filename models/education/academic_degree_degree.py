from sqlalchemy.orm import relationship

from models import NamedModel


class AcademicDegreeDegree(NamedModel):

    __tablename__ = "hr_erp_academic_degree_degrees"

    academic_degree = relationship("AcademicDegree", back_populates="degree")

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey

from models import NamedModel


class AcademicDegreeDegree(NamedModel):

    __tablename__ = "dic_hr_erp_academic_degree_degrees"
    # parent_id = Column(String(), ForeignKey("hr_erp_academic_degree_degrees.id"), nullable=True)
    #academic_degree_id = Column(String(), ForeignKey("hr_erp_academic_degrees.id"), nullable=True)

    # children = relationship("AcademicDegreeDegree", back_populates="parent")
    academic_degree = relationship("AcademicDegree", back_populates="degree")

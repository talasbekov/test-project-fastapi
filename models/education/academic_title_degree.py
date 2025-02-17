from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey

from models import NamedModel


class AcademicTitleDegree(NamedModel):

    __tablename__ = "hr_erp_academic_title_degrees"
    # parent_id = Column(String(), ForeignKey("hr_erp_academic_title_degrees.id"), nullable=True)

    academic_title = relationship("AcademicTitle", back_populates="degree")

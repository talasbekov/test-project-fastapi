from sqlalchemy.orm import relationship

from models import NamedModel


class Specialty(NamedModel):

    __tablename__ = "specialties"

    academic_title = relationship("AcademicTitle", back_populates="specialty")
    academic_degree = relationship("AcademicDegree", back_populates="specialty")
    education = relationship("Education", back_populates="specialty")

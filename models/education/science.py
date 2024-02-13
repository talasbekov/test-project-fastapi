from sqlalchemy.orm import relationship

from models import NamedModel


class Science(NamedModel):

    __tablename__ = "hr_erp_sciences"

    academic_degree = relationship("AcademicDegree", back_populates="science")

from sqlalchemy.orm import relationship

from models import NamedModel


class AcademicTitleDegree(NamedModel):

    __tablename__ = "academic_title_degrees"

    academic_title = relationship("AcademicTitle", back_populates="degree")

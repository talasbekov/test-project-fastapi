from sqlalchemy.orm import relationship

from core import Base
from models import Model


class Profile(Model, Base):

    __tablename__ = "profiles"

    academic_degree = relationship("AcademicDegree")
    academic_title = relationship("AcademicTitle")
    education = relationship("Education")
    course = relationship("Course")
    language_proficiency = relationship("LanguageProficiency")
    educational_profile = relationship("EducationalProfile")

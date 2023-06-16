import enum

from sqlalchemy.orm import relationship

from models import NamedModel


class SurveyTypeEnum(str, enum.Enum):
    REGULAR = "Обычный"
    ANONYMOUS = "Анонимный"


class SurveyType(NamedModel):

    __tablename__ = "survey_types"

    surveys = relationship("Survey", cascade="all,delete", back_populates="type")
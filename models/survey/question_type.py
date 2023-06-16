import enum

from models import NamedModel
from sqlalchemy.orm import relationship


class QuestionTypeEnum(str, enum.Enum):
    TEXT = "Текст"
    SINGLE_CHOICE = "Один из списка"
    MULTIPLE_CHOICE = "Несколько из списка"
    SCALE = "Шкала"
    GRID = "Сетка"
    CHECKBOX_GRID = "Сетка флажков"


class QuestionType(NamedModel):

    __tablename__ = "question_types"
    
    questions = relationship("Question", cascade="all,delete", back_populates="question_type")

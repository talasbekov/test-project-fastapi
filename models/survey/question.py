import enum

from sqlalchemy import Column, ForeignKey, Boolean, TEXT, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class QuestionTypeEnum(str, enum.Enum):
    TEXT = "Текст"
    SINGLE_SELECTION = "Один из списка"
    MULTIPLE_SELECTION = "Несколько из списка"
    SCALE = "Шкала"
    GRID = "Сетка"
    CHECKBOX_GRID = "Сетка флажков"


class Question(Model):

    __tablename__ = "questions"

    text = Column(TEXT, nullable=False)
    is_required = Column(Boolean, nullable=False, default=True)
    survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.id"))
    question_type = Column(Enum(QuestionTypeEnum), nullable=False)

    survey = relationship("Survey", foreign_keys=[
                          survey_id], back_populates="questions")
    options = relationship("Option", cascade="all,delete",
                           back_populates="question")
    answers = relationship("Answer", cascade="all, delete",
                           back_populates="question")

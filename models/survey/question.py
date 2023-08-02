import enum

from sqlalchemy import Column, ForeignKey, Boolean, TEXT, Enum, Integer, String
from sqlalchemy.orm import relationship

from models import TextModel


class QuestionTypeEnum(str, enum.Enum):
    TEXT = "Текст"
    SINGLE_SELECTION = "Один из списка"
    MULTIPLE_SELECTION = "Несколько из списка"


class Question(TextModel):

    __tablename__ = "questions"

    is_required = Column(Boolean, nullable=False, default=True)
    question_type = Column(Enum(QuestionTypeEnum), nullable=False)
    diagram_description = Column(TEXT, nullable=True)
    report_description = Column(TEXT, nullable=True)
    survey_id = Column(String(), ForeignKey("surveys.id"), nullable=True)
    score = Column(Integer, nullable=True)

    options = relationship("Option", cascade="all,delete",
                           back_populates="question")
    answers = relationship("Answer", cascade="all, delete",
                           back_populates="question")
    survey = relationship("Survey", foreign_keys=[
                          survey_id], back_populates="questions")

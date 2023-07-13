import enum

from sqlalchemy import Column, ForeignKey, Boolean, TEXT, Enum, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import TextModel


class QuestionTypeEnum(str, enum.Enum):
    TEXT = "Текст"
    SINGLE_SELECTION = "Один из списка"
    MULTIPLE_SELECTION = "Несколько из списка"


class QuestionBase(TextModel):

    __tablename__ = "questions"

    is_required = Column(Boolean, nullable=False, default=True)
    question_type = Column(Enum(QuestionTypeEnum), nullable=False)
    discriminator = Column(String(255), nullable=True)
    diagram_description = Column(TEXT, nullable=True)
    report_description = Column(TEXT, nullable=True)

    options = relationship("Option", cascade="all,delete",
                           back_populates="question")
    answers = relationship("Answer", cascade="all, delete",
                           back_populates="question")

    __mapper_args__ = {
        "polymorphic_on": discriminator,
        "polymorphic_identity": "questions"
    }


class QuestionSurvey(QuestionBase):

    survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.id"), nullable=True)

    survey = relationship("Survey", foreign_keys=[
                          survey_id], back_populates="questions")

    __mapper_args__ = {
        "polymorphic_identity": "question_survey"
    }


class QuestionQuiz(QuestionBase):

    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"), nullable=True)
    score = Column(Integer, nullable=True)

    quiz = relationship("Quiz", foreign_keys=[
                          quiz_id], back_populates="questions")

    __mapper_args__ = {
        "polymorphic_identity": "question_quiz"
    }

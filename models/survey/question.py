from sqlalchemy import Column, ForeignKey, Boolean, String, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class Question(Model):

    __tablename__ = "questions"

    text = Column(TEXT, nullable=False)
    is_required = Column(Boolean, nullable=False, default=True)
    survey_id = Column(UUID(as_uuid=True), ForeignKey("surveys.id"))
    question_type_id = Column(UUID(as_uuid=True), ForeignKey("question_types.id"))
    discriminator = Column(String(255))

    survey = relationship("Survey", foreign_keys=[survey_id], back_populates="questions")
    question_type = relationship("QuestionType", foreign_keys=[question_type_id], back_populates="questions")
    options = relationship("OptionText", cascade="all,delete", back_populates="question")
    answers = relationship("Answer", cascade="all, delete", back_populates="question")

    __mapper_args__ = {
        "polymorphic_on": discriminator,
        "polymorphic_identity": "question",
    }


class QuestionText(Question):

    __mapper_args__ = {
        "polymorphic_identity": "question_text"
    }


class QuestionSingleChoice(Question):

    __mapper_args__ = {
        "polymorphic_identity": "question_single_choice"
    }


class QuestionMultipleChoice(Question):

    __mapper_args__ = {
        "polymorphic_identity": "question_multiple_choice"
    }


class QuestionScale(Question):
    options = relationship("OptionScale", cascade="all,delete", back_populates="question")
    
    __mapper_args__ = {
        "polymorphic_identity": "question_scale"
    }


class QuestionGrid(Question):
    options = relationship("OptionGrid", cascade="all,delete", back_populates="question")

    __mapper_args__ = {
        "polymorphic_identity": "question_grid"
    }


class QuestionCheckboxGrid(Question):
    options = relationship("OptionCheckboxGrid", cascade="all,delete", back_populates="question")
    
    __mapper_args__ = {
        "polymorphic_identity": "question_checkbox_grid"
    }

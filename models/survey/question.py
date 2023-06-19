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

    survey = relationship("Survey", foreign_keys=[survey_id], back_populates="questions")
    question_type = relationship("QuestionType", foreign_keys=[question_type_id], back_populates="questions")
    options = relationship("Option", cascade="all,delete", back_populates="question")
    answers = relationship("Answer", cascade="all, delete", back_populates="question")

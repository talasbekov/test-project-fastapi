from sqlalchemy import Column, ForeignKey, String, TEXT, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
from models.association import answers_options


class Answer(Model):

    __tablename__ = "answers"

    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))
    discriminator = Column(String(255))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    question = relationship("QuestionBase", foreign_keys=[
                            question_id], back_populates="answers")
    user = relationship("User", foreign_keys=[
                        user_id], back_populates="answers")
    options = relationship(
        "Option", secondary=answers_options, back_populates="answers")

    __mapper_args__ = {
        "polymorphic_on": discriminator,
        "polymorphic_identity": "answers"
    }


class AnswerText(Answer):
    text = Column(TEXT, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "answer_text"
    }


class AnswerSingleSelection(Answer):
    option_id = Column(UUID(as_uuid=True), ForeignKey(
        "options.id"), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "answer_single_choice"
    }


class AnswerScale(Answer):
    scale_value = Column(Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "answer_scale"
    }


class AnswerGrid(Answer):
    grid_values = Column(JSON, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "answer_grid"
    }


class AnswerCheckboxGrid(Answer):
    checkbox_grid_values = Column(JSON, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'answer_checkbox_grid',
    }

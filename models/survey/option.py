from sqlalchemy import TEXT, Integer, Column, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
from models.association import answers_options


class Option(Model):

    __tablename__ = "options"

    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))
    text = Column(TEXT, nullable = True)
    discriminator = Column(String(255))

    question = relationship("Question", foreign_keys=[question_id], back_populates="options")

    __mapper_args__ = {
        "polymorphic_on": discriminator,
        "polymorphic_identity": "options"
    }
    

class OptionMultipleChoice(Option):
    answers = relationship("Answer", secondary=answers_options, back_populates="answers")

    __mapper_args__ = {
        "polymorphic_identity": "option_multiple_choice"
    }


class OptionScale(Option):
    min_value = Column(Integer, nullable=False)
    max_value = Column(Integer, nullable=False)

    question = relationship("QuestionScale", foreign_keys=[Option.question_id], back_populates="options")

    __mapper_args__ = {
        "polymorphic_identity": "option_scale"
    }


class OptionGrid(Option):
    row_position = Column(Integer, nullable=False)
    column_position = Column(Integer, nullable=False)

    question = relationship("QuestionGrid", foreign_keys=[Option.question_id], back_populates="options")

    __mapper_args__ = {
        "polymorphic_identity": "option_grid"
    }


class OptionCheckboxGrid(OptionGrid):
    is_checked = Column(Boolean, default=False, nullable=False)

    question = relationship("QuestionCheckboxGrid", foreign_keys=[Option.question_id], back_populates="options")

    __mapper_args__ = {
        "polymorphic_identity": "option_checkbox_grid"
    }

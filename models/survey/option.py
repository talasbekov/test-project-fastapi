from sqlalchemy import TEXT, Integer, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
from models.association import answers_options


class Option(Model):

    __tablename__ = "options"

    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))
    discriminator = Column(String(255), nullable=True)
    score = Column(Integer, nullable=True)

    question = relationship("QuestionBase", foreign_keys=[
                            question_id], back_populates="options")
    answers = relationship(
        "Answer", secondary=answers_options, back_populates="options")

    __mapper_args__ = {
        "polymorphic_on": discriminator,
        "polymorphic_identity": "options"
    }


class OptionText(Option):
    text = Column(TEXT, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "option_text"
    }


class OptionScale(Option):
    min_value = Column(Integer, nullable=True)
    max_value = Column(Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "option_scale"
    }


class OptionGrid(Option):
    row_position = Column(Integer, nullable=True)
    column_position = Column(Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "option_grid"
    }


class OptionCheckboxGrid(OptionGrid):

    __mapper_args__ = {
        "polymorphic_identity": "option_checkbox_grid"
    }

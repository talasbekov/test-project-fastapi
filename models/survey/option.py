from sqlalchemy import TEXT, Integer, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import TextModel
from models.association import answers_options


class Option(TextModel):

    __tablename__ = "options"

    text = Column(TEXT, nullable=True)

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

    __mapper_args__ = {
        "polymorphic_identity": "option_text"
    }

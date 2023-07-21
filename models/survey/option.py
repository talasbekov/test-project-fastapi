from sqlalchemy import TEXT, Integer, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import object_session

from models import TextModel
from models.association import answers_options
from .answer import Answer, AnswerSingleSelection


class Option(TextModel):

    __tablename__ = "options"

    text = Column(TEXT, nullable=True)

    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))
    score = Column(Integer, nullable=True)

    question = relationship("Question", foreign_keys=[
                            question_id], back_populates="options")
    answers = relationship(
        "Answer", secondary=answers_options, back_populates="options")

    @property
    def answer_count(self):
        return object_session(self).query(Answer).filter(
            (AnswerSingleSelection.option_id == self.id) |
            (Answer.options.contains(self))
        ).count()

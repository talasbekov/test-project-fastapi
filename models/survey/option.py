from sqlalchemy import TEXT, Integer, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import TextModel
from models.association import answers_options


class Option(TextModel):

    __tablename__ = "hr_erp_options"

    text = Column(TEXT, nullable=True)

    question_id = Column(String(), ForeignKey("hr_erp_questions.id"))
    score = Column(Integer, nullable=True)

    question = relationship("Question", foreign_keys=[
                            question_id], back_populates="options")
    answers = relationship(
        "Answer", secondary=answers_options, back_populates="options")


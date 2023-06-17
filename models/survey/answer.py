from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
from models.association import answers_options


class Answer(Model):

    __tablename__ = "answers"

    question_id = Column(UUID(as_uuid=True), ForeignKey("survey_types.id"))

    question = relationship("Question", foreign_keys=[question_id], back_populates="answers")
    options = relationship("Option", secondary=answers_options, back_populates="answers")

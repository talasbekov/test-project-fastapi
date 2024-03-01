from sqlalchemy import Column, ForeignKey, String, CLOB, Integer
from sqlalchemy.orm import relationship

from models import Model
from models.association import answers_options


class Answer(Model):

    __tablename__ = "hr_erp_answers"

    question_id = Column(String(), ForeignKey("hr_erp_questions.id"))
    discriminator = Column(String(255))
    user_id = Column(String(), ForeignKey("hr_erp_users.id"), nullable=True)
    encrypted_used_id = Column(String(255), nullable=True)
    score = Column(Integer, nullable=True)

    question = relationship("Question", foreign_keys=[
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
    text = Column(CLOB, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "answer_text"
    }

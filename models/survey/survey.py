from sqlalchemy import Column, ForeignKey, TEXT, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class Base(NamedModel):

    __abstract__ = True

    description = Column(TEXT, nullable=True)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    jurisdiction_id = Column(
        UUID(as_uuid=True), ForeignKey("jurisdictions.id"))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))


class Survey(Base):

    __tablename__ = "surveys"

    is_anonymous = Column(Boolean(), default=False, nullable=True)

    questions = relationship(
        "QuestionSurvey", cascade="all, delete", back_populates="survey")


class Quiz(Base):

    __tablename__ = "quizzes"

    questions = relationship(
        "QuestionQuiz", cascade="all, delete", back_populates="quiz")

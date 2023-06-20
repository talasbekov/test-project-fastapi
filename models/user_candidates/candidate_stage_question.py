import enum

from sqlalchemy import Column, String, ForeignKey, Enum, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class CandidateStageQuestionTypeEnum(str, enum.Enum):
    STRING_TYPE = "String"
    CHOICE_TYPE = "Choice"
    TEXT_TYPE = "Text"
    DOCUMENT_TYPE = "Document"
    ESSAY_TYPE = "Essay"
    SPORT_SCORE_TYPE = "Sport score"
    DROPDOWN_TYPE = "Dropdown"


class CandidateStageQuestion(Model):

    __tablename__ = "candidate_stage_questions"
    question = Column(String, nullable=True)
    question_type = Column(Enum(CandidateStageQuestionTypeEnum), nullable=True)
    description = Column(TEXT, nullable=True)

    candidate_stage_type_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey("candidate_stage_types.id"),
        nullable=True)
    candidate_stage_type = relationship(
        "CandidateStageType",
        back_populates="candidate_stage_questions",
        foreign_keys=candidate_stage_type_id)

    candidate_stage_answers = relationship(
        "CandidateStageAnswer",
        back_populates="candidate_stage_question",
        cascade="all, delete")

from sqlalchemy import Column, String, ForeignKey, Boolean, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
from models.user_candidates import CandidateStageQuestionTypeEnum


class CandidateStageAnswer(Model):

    __tablename__ = "candidate_stage_answers"

    candidate_stage_question_id = Column(
        String(),
        ForeignKey("candidate_stage_questions.id"),
        nullable=True)
    candidate_stage_question = relationship(
        "CandidateStageQuestion",
        back_populates="candidate_stage_answers",
        foreign_keys=candidate_stage_question_id)

    candidate_id = Column(
        String(),
        ForeignKey("candidates.id"),
        nullable=True)
    candidate = relationship(
        "Candidate",
        back_populates="candidate_stage_answers",
        foreign_keys=candidate_id)

    type = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "candidate_stage_answer",
        "polymorphic_on": type,
    }


class CandidateStageAnswerDefault(CandidateStageAnswer):

    answer_str = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': CandidateStageQuestionTypeEnum.STRING_TYPE.value,
    }


class CandidateStageAnswerChoice(CandidateStageAnswer):

    answer_bool = Column(Boolean, nullable=True)
    document_number = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': CandidateStageQuestionTypeEnum.CHOICE_TYPE.value,
    }


class CandidateStageAnswerText(CandidateStageAnswer):

    answer = Column(TEXT, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': CandidateStageQuestionTypeEnum.TEXT_TYPE.value,
    }


class CandidateStageAnswerDocument(CandidateStageAnswer):

    document_link = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': CandidateStageQuestionTypeEnum.DOCUMENT_TYPE.value,
    }


class CandidateEssayAnswer(CandidateStageAnswer):

    candidate_essay_type_id = Column(
        String(),
        ForeignKey("candidate_essay_types.id"),
        nullable=True)
    candidate_essay_type = relationship(
        "CandidateEssayType",
        back_populates="candidate_essay_answers",
        foreign_keys=candidate_essay_type_id)

    __mapper_args__ = {
        'polymorphic_identity': CandidateStageQuestionTypeEnum.ESSAY_TYPE.value,
    }


class CandidateSportAnswer(CandidateStageAnswer):
    is_sport_passed = Column(Boolean, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': CandidateStageQuestionTypeEnum.SPORT_SCORE_TYPE.value,
    }


class CandidateDropdownAnswer(CandidateStageAnswer):
    category_id = Column(String(), ForeignKey(
        "candidate_categories.id"), nullable=True)
    category = relationship("CandidateCategory", cascade="all, delete")

    __mapper_args__ = {
        'polymorphic_identity': CandidateStageQuestionTypeEnum.DROPDOWN_TYPE.value,
    }

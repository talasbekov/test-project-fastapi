from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
 

class CandidateStageAnswer(Model):

    __tablename__ = "candidate_stage_answers"

    candidate_stage_question_id = Column(UUID(as_uuid=True), ForeignKey("candidate_stage_questions.id"), nullable=True)
    candidate_stage_question = relationship("CandidateStageQuestion", back_populates="candidate_stage_answers", foreign_keys=candidate_stage_question_id)

    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=True)
    candidate = relationship("Candidate", back_populates="candidate_stage_answers", foreign_keys=candidate_id)

    type = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "candidate_stage_answer",
        "polymorphic_on": type,
    }

class CandidateStageAnswerDefault(CandidateStageAnswer):    

    answer_str = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'candidate_stage_answer_string',
    }


class CandidateStageAnswerChoice(CandidateStageAnswer):
    
    answer_bool = Column(Boolean, nullable=True)
    document_number = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'candidate_stage_answer_choice',
    }


class CandidateStageAnswerText(CandidateStageAnswer):
         
    answer = Column(TEXT, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'candidate_stage_answer_text',
    }


class CandidateStageAnswerDocument(CandidateStageAnswer):
    
    document_link = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'candidate_stage_answer_document', 
    }


class CandidateEssayAnswer(CandidateStageAnswer):
 
    candidate_essay_type_id = Column(UUID(as_uuid=True), ForeignKey("candidate_essay_types.id"), nullable=True)
    candidate_essay_type = relationship("CandidateEssayType", back_populates="candidate_essay_answers", foreign_keys=candidate_essay_type_id)

    __mapper_args__ = {
        'polymorphic_identity': 'candidate_essay_answer',
    }


class CandidateSportAnswer(CandidateStageAnswer):
    is_sport_passed = Column(Boolean, nullable=True)


    __mapper_args__ = {
        'polymorphic_identity': 'candidate_sport_answer',
    }

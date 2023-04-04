from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel

class CandidateStageType(NamedModel):

    __tablename__ = "candidate_stage_types"

    is_curator_review_required = Column(Boolean, nullable=True)
    candidate_stage_infos = relationship("CandidateStageInfo", back_populates="candidate_stage_type")  
    candidate_stage_questions = relationship("CandidateStageQuestion", back_populates="candidate_stage_type")

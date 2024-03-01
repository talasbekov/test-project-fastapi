from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer

from models import NamedModel


class CandidateStageType(NamedModel):

    __tablename__ = "hr_erp_candidate_stage_types"
    
    stage_order = Column(Integer)
    candidate_stage_infos = relationship(
        "CandidateStageInfo",
        back_populates="candidate_stage_type")
    cand_stage_questions = relationship(
        "CandidateStageQuestion",
        back_populates="candidate_stage_type")

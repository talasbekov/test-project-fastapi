from sqlalchemy import Column, Boolean
from sqlalchemy.orm import relationship

from models import NamedModel


class CandidateStageType(NamedModel):

    __tablename__ = "candidate_stage_types"

    candidate_stage_infos = relationship("CandidateStageInfo", back_populates="candidate_stage_type")
    candidate_stage_questions = relationship("CandidateStageQuestion", back_populates="candidate_stage_type")
    
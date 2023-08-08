from sqlalchemy.orm import relationship

from models import NamedModel


class CandidateStageType(NamedModel):

    __tablename__ = "hr_erp_candidate_stage_types"

    candidate_stage_infos = relationship(
        "CandidateStageInfo",
        back_populates="candidate_stage_type")
    cand_stage_questions = relationship(
        "CandidateStageQuestion",
        back_populates="candidate_stage_type")

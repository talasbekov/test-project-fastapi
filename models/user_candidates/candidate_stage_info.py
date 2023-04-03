from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
 

class CandidateStageInfo(Model):

    __tablename__ = "candidate_stage_infos"

    status = Column(String, nullable=True)
    date_sign = Column(TIMESTAMP, nullable=True, default=None)
    candidate_stage_type_id = Column(UUID(as_uuid=True), ForeignKey("candidate_stage_types.id"), nullable=True)
    candidate_stage_type = relationship("CandidateStageType", back_populates="candidate_stage_infos", foreign_keys=candidate_stage_type_id, uselist=False)
    staff_unit_coordinate_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"), nullable=True)
    is_waits = Column(Boolean, nullable=True, default=False)

    candidate_stage_id = Column(UUID(as_uuid=True), ForeignKey("candidate_stages.id"), nullable=True)
    candidate_stage = relationship("CandidateStage", back_populates="candidate_stage_info", foreign_keys=candidate_stage_id, uselist=False)

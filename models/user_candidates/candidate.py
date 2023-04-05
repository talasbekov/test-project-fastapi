from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class Candidate(Model):

    __tablename__ = "candidates"

    staff_unit_curator_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"), nullable=True)
    staff_unit_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"), nullable=True)
    essay_id = Column(UUID(as_uuid=True), ForeignKey("candidate_essay_types.id"), nullable=True)

    staff_unit_curator = relationship("StaffUnit", foreign_keys=staff_unit_curator_id)
    staff_unit = relationship("StaffUnit", foreign_keys=staff_unit_id)

    essay = relationship("CandidateEssayType", cascade="all, delete")
    candidate_stage_answers = relationship("CandidateStageAnswer", back_populates="candidate", cascade="all, delete")
    candidate_stage_infos = relationship("CandidateStageInfo", back_populates="candidate", cascade="all, delete")

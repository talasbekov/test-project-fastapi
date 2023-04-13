import enum

from sqlalchemy import Column, ForeignKey, TIMESTAMP, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class CandidateStageInfoStatusEnum(str, enum.Enum):
    PENDING = "В прогрессе"
    APPROVED = "Пройден успешно"
    DECLINED = "Завален"
    NOT_STARTED = "Не начат"


class CandidateStageInfo(Model):

    __tablename__ = "candidate_stage_infos"

    status = Column(Enum(CandidateStageInfoStatusEnum), nullable=True, server_default=CandidateStageInfoStatusEnum.NOT_STARTED.value)
    date_sign = Column(TIMESTAMP, nullable=True, default=None)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=True)
    candidate_stage_type_id = Column(UUID(as_uuid=True), ForeignKey("candidate_stage_types.id"), nullable=True)
    candidate_stage_type = relationship("CandidateStageType", back_populates="candidate_stage_infos")
    
    staff_unit_coordinate_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"), nullable=True)
    is_waits = Column(Boolean, nullable=True, default=True)

    candidate = relationship("Candidate", back_populates="candidate_stage_infos")
    staff_unit_coordinate = relationship("StaffUnit", cascade="all, delete")

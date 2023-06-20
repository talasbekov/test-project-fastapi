import enum

from sqlalchemy import Column, ForeignKey, Enum, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates

from models import Model


class CandidateStatusEnum(str, enum.Enum):
    ACTIVE = "Активный"
    DRAFT = "Черновик"


class Candidate(Model):

    __tablename__ = "candidates"

    status = Column(Enum(CandidateStatusEnum),
                    server_default=CandidateStatusEnum.ACTIVE)
    debarment_reason = Column(String, nullable=True)
    is_physical_passed = Column(Boolean, nullable=True)
    attempt_number = Column(Integer, server_default='0', nullable=True)
    staff_unit_curator_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey("staff_units.id"),
        nullable=True)
    staff_unit_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey("staff_units.id"),
        nullable=True)
    essay_id = Column(UUID(as_uuid=True), ForeignKey(
        "candidate_essay_types.id"), nullable=True)
    recommended_by = Column(
        UUID(
            as_uuid=True),
        ForeignKey("users.id"),
        nullable=True)

    staff_unit_curator = relationship(
        "StaffUnit", foreign_keys=staff_unit_curator_id)
    staff_unit = relationship("StaffUnit", foreign_keys=staff_unit_id)

    essay = relationship("CandidateEssayType", cascade="all, delete")
    candidate_stage_answers = relationship(
        "CandidateStageAnswer",
        back_populates="candidate",
        cascade="all, delete")
    candidate_stage_infos = relationship(
        "CandidateStageInfo",
        back_populates="candidate",
        cascade="all, delete")
    recommended_by_user = relationship("User", foreign_keys=recommended_by)

    @validates('debarment_reason')
    def validate_debarment_reason(self, key, value):
        if self.status == CandidateStatusEnum.ACTIVE:
            if value is not None:
                raise ValueError(
                    "debarment_reason должен быть пустым для статуса Активный")
        elif self.status == CandidateStatusEnum.DRAFT:
            if value is None:
                raise ValueError(
                    "debarment_reason обязателен для статуса Архивный")
        return value

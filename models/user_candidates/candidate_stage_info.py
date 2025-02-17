import enum

from sqlalchemy import Column, ForeignKey, TIMESTAMP, Boolean, Enum, String
from sqlalchemy.orm import relationship

from models import Model
from models.association import s_u_cand_stage_infos
from models.archive.association import a_s_u_cand_stage_infos


class CandidateStageInfoStatusEnum(str, enum.Enum):
    PENDING = "В прогрессе"
    APPROVED = "Пройден успешно"
    DECLINED = "Завален"
    NOT_STARTED = "Не начат"


class CandidateStageInfo(Model):

    __tablename__ = "hr_erp_candidate_stage_infos"

    status = Column(
        Enum(CandidateStageInfoStatusEnum),
        nullable=True,
        default=CandidateStageInfoStatusEnum.NOT_STARTED.value)
    date_sign = Column(TIMESTAMP(timezone=True), nullable=True, default=None)
    candidate_id = Column(
        String(),
        ForeignKey("hr_erp_candidates.id"),
        nullable=True)
    candidate_stage_type_id = Column(
        String(),
        ForeignKey("hr_erp_candidate_stage_types.id"),
        nullable=True)
    candidate_stage_type = relationship(
        "CandidateStageType",
        back_populates="candidate_stage_infos")

    is_waits = Column(Boolean, nullable=True, default=True)

    candidate = relationship("Candidate",
                             back_populates="candidate_stage_infos")
    staff_unit_coordinate_ids = relationship(
        "StaffUnit",
        secondary=s_u_cand_stage_infos,
        back_populates="candidate_stage_infos",
        cascade="all,delete",
    )

    archive_staff_unit_coordinate_ids = relationship(
        "ArchiveStaffUnit",
        secondary=a_s_u_cand_stage_infos,
        back_populates="candidate_stage_infos",
        cascade="all,delete",
    )

import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from models import CandidateStageInfo
from models import CandidateStageInfoStatusEnum
from schemas import (CandidateStageInfoRead, CandidateStageInfoCreate, CandidateStageInfoUpdate)
from services import ServiceBase


class CandidateStageInfoService(ServiceBase[CandidateStageInfo, CandidateStageInfoCreate, CandidateStageInfoUpdate]):

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ):
        return db.query(self.model).order_by(self.model.id.asc()).offset(skip).limit(limit).all()
    
    def get_all_by_staff_unit_id(self, db: Session, skip: int, limit: int, staff_unit_id: str):
        candidates = db.query(CandidateStageInfo).filter(
            CandidateStageInfo.staff_unit_coordinate_id == staff_unit_id,
            CandidateStageInfo.is_waits == True
        ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()
        candidates = [CandidateStageInfoRead.from_orm(candidate).dict() for candidate in candidates]
        return candidates

    def get_all_by_candidate_id(self, db: Session, skip: int, limit: int, candidate_id: uuid.UUID):
        return db.query(CandidateStageInfo).filter(
            CandidateStageInfo.candidate_id == candidate_id,
        ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()

    def sign_candidate(self, db: Session, id: uuid.UUID):
        candidate: CandidateStageInfo = super().get_by_id(db, id)

        candidate.status = CandidateStageInfoStatusEnum.APPROVED.value
        candidate.is_waits = False
        candidate.date_sign = datetime.now()  # set the current date to the date_sign field

        db.add(candidate)
        db.flush()

        return candidate

    def reject_candidate(self, db: Session, id: uuid.UUID):
        candidate = super().get_by_id(db, id)

        candidate.status = CandidateStageInfoStatusEnum.DECLINED.value
        candidate.is_waits = False
        candidate.date_sign = datetime.now()  # set the current date to the date_sign field

        db.add(candidate)
        db.flush()

        return candidate


candidate_stage_info_service = CandidateStageInfoService(CandidateStageInfo) # type: ignore

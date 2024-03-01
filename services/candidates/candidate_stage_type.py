from sqlalchemy.orm import Session

from models import CandidateStageType
from schemas import CandidateStageTypeCreate, CandidateStageTypeUpdate
from services import ServiceBase


class CandidateStageTypeService(
        ServiceBase[CandidateStageType,
                    CandidateStageTypeCreate,
                    CandidateStageTypeUpdate]):

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ):
        return db.query(self.model).order_by(
            self.model.stage_order).offset(skip).limit(limit).all()
        
    def get_count(
        self, db: Session
    ):
        return db.query(self.model).count()


candidate_stage_type_service = CandidateStageTypeService(
    CandidateStageType)  # type: ignore

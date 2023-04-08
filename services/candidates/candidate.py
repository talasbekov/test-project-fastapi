from sqlalchemy.orm import Session

from models import Candidate, CandidateStageInfo, CandidateStageType
from models import CandidateStageInfoStatusEnum
from schemas import CandidateCreate, CandidateUpdate
from schemas import CandidateRead
from services import ServiceBase, staff_unit_service


class CandidateService(ServiceBase[Candidate, CandidateCreate, CandidateUpdate]):
    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100):
        candidates = super().get_multi(db, skip, limit)     
        candidates = [CandidateRead.from_orm(candidate).dict() for candidate in candidates]
        for candidate in candidates: 
            candidate_stage_info_count = db.query(CandidateStageType).count()

            candidate_stage_info_success_count = db.query(
                CandidateStageInfo).filter( 
                CandidateStageInfo.status == CandidateStageInfoStatusEnum.APPROVED.value,
                CandidateStageInfo.candidate_id == candidate['id']
            ).count()

            candidate['progress'] = candidate_stage_info_success_count / candidate_stage_info_count * 100 if candidate_stage_info_count > 0 else 0
            
            current_stage_info = db.query(CandidateStageInfo).filter(
                CandidateStageInfo.status == CandidateStageInfoStatusEnum.PENDING.value,
                CandidateStageInfo.candidate_id == candidate['id']
            ).order_by(CandidateStageInfo.created_at.desc()).first()
            
            if current_stage_info:
                candidate['current_stage'] = current_stage_info.id
            candidate_obj = super().get_by_id(db, candidate['id'])
            if candidate_obj.candidate_stage_answers:
                candidate['last_edit_date'] = candidate_obj.candidate_stage_answers[0].created_at
        return candidates

    def create(self, db: Session, body: CandidateCreate):
        staff_unit_service.get_by_id(db, body.staff_unit_curator_id)
        staff_unit_service.get_by_id(db, body.staff_unit_id)

        return super().create(db, body)

    def update(self, db: Session, id: str, body: CandidateUpdate):
        staff_unit_service.get_by_id(db, body.staff_unit_curator_id)
        staff_unit_service.get_by_id(db, body.staff_unit_id)

        return super().update(db, db_obj=super().get_by_id(db, id), obj_in=body)


candidate_service = CandidateService(Candidate) # type: ignore

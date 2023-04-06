from sqlalchemy.orm import Session

from models import Candidate, CandidateStageInfo, CandidateStageType
from models import CandidateStageInfoStatusEnum
from schemas import CandidateCreate, CandidateUpdate
from schemas import CandidateRead
from services import ServiceBase, staff_unit_service
from .candidate_essay_type import candidate_essay_type_service
from models import CandidateStatusEnum


class CandidateService(ServiceBase[Candidate, CandidateCreate, CandidateUpdate]):
    def get_multiple(self, db: Session, skip: int = 0, limit: int = 100):

        candidates = db.query(self.model).filter(
            self.model.status == CandidateStatusEnum.ACTIVE.value
        ).offset(skip).limit(limit).all()

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

    def get_draft_candidates(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(
            self.model.status == CandidateStatusEnum.DRAFT.value
        ).offset(skip).limit(limit).all()

    def create(self, db: Session, body: CandidateCreate):
        staff_unit_service.get_by_id(db, body.staff_unit_curator_id)
        staff_unit_service.get_by_id(db, body.staff_unit_id)

        return super().create(db, body)

    def update(self, db: Session, id: str, body: CandidateUpdate):

        candidate = candidate_service.get_by_id(db, id)

        if body.staff_unit_id is not None:
            staff_unit_service.get_by_id(db, body.staff_unit_id)
            candidate.staff_unit_id = body.staff_unit_id
        if body.staff_unit_curator_id is not None:
            staff_unit_service.get_by_id(db, body.staff_unit_curator_id)
            candidate.staff_unit_curator_id = body.staff_unit_curator_id
        if body.status is not None:
            candidate.status = body.status

        db.add(candidate)
        db.flush()

        return candidate

    def update_essay(self, db: Session, id: str, essay_id: str):
        candidate = self.get_by_id(db, id)
        essay = candidate_essay_type_service.get_by_id(db, essay_id)

        candidate.essay_id = essay_id

        db.add(candidate)
        db.flush()

        return candidate


candidate_service = CandidateService(Candidate) # type: ignore

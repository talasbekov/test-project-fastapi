import uuid
from typing import List

from sqlalchemy.orm import Session

from models import Candidate, CandidateStageInfo, CandidateStageType
from models import CandidateStageInfoStatusEnum
from schemas import CandidateCreate, CandidateUpdate
from schemas import CandidateRead
from services import ServiceBase, staff_unit_service, user_service
from .candidate_essay_type import candidate_essay_type_service
from models import CandidateStatusEnum, Position


class CandidateService(ServiceBase[Candidate, CandidateCreate, CandidateUpdate]):
    def get_multiple(self, db: Session, user_id: str, role_id: str, skip: int = 0, limit: int = 100):

        if self._check_by_role(db, role_id):
            candidates = db.query(self.model).filter(
                self.model.status == CandidateStatusEnum.ACTIVE.value
            ).offset(skip).limit(limit).all()
        else:
            candidates = self._get_supervised_active_candidates(db, user_id)

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

    def get_draft_candidates(self, db: Session, user_id: str, role_id: str, skip: int = 0, limit: int = 100):

        if self._check_by_role(db, role_id):
            return db.query(self.model).filter(
                self.model.status == CandidateStatusEnum.DRAFT.value
            ).offset(skip).limit(limit).all()
        else:
            return self._get_supervised_draft_candidates(db, user_id)

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

    def _check_by_role(self, db: Session, role_id: str) -> bool:
        staff_unit = staff_unit_service.get_by_id(db, role_id)

        available_all = {
            'Начальник кадров',
            'Заместители начальника кадров',
            'Начальник управления кандидатами',
            'Политический гос. служащий'
        }

        available_all_roles = []

        for i in available_all:
            available_all_roles.append(self._get_role_by_name(db, i))

        for i in available_all_roles:
            if staff_unit.position_id == i:
                return True

        return False

    def _get_role_by_name(self, db: Session, name: str) -> Position:
        role = db.query(Position).filter(
            Position.name == name
        ).first()

        if role:
            return role.id
        else:
            return None

    def _get_supervised_active_candidates(self, db: Session, user_id: str):
        user = user_service.get_by_id(db, user_id)

        return db.query(self.model).filter(
            self.model.staff_unit_curator_id == user.actual_staff_unit_id,
            self.model.status == CandidateStatusEnum.ACTIVE.value
        ).all()

    def _get_supervised_draft_candidates(self, db: Session, user_id: str):
        user = user_service.get_by_id(db, user_id)

        return db.query(self.model).filter(
            self.model.staff_unit_curator_id == user.actual_staff_unit_id,
            self.model.status == CandidateStatusEnum.DRAFT.value
        ).all()


candidate_service = CandidateService(Candidate) # type: ignore

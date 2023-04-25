from fastapi.logger import logger as log
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from exceptions import NotFoundException, ForbiddenException, BadRequestException
from models import (Candidate, CandidateStageInfo, StaffUnit, User,
                    CandidateStatusEnum, Position, CandidateStageType,
                    PositionNameEnum, CandidateStageInfoStatusEnum)
from schemas import CandidateCreate, CandidateUpdate, CandidateRead, CandidateStageInfoCreate, UserCreate, CandidateEssayUpdate, CandidateEssayTypeCreate
from services import ServiceBase, staff_unit_service, user_service, position_service
from .candidate_essay_type import candidate_essay_type_service
from .candidate_stage_info import candidate_stage_info_service


class CandidateService(ServiceBase[Candidate, CandidateCreate, CandidateUpdate]):

    # This const variable stores the positions which have access to all candidates
    ALL_CANDIDATE_VIEWERS = {
        PositionNameEnum.PERSONNEL_HEAD.value,
        PositionNameEnum.DEPUTY_PERSONNEL_HEAD.value,
        PositionNameEnum.CANDIDATE_MANAGEMENT_HEAD.value,
        PositionNameEnum.POLITICS_GOVERNMENT_SERVANT.value
    }

    def get_multiple(self, db: Session,
                     filter: str,
                     user_id: str,
                     role_id: str,
                     skip: int = 0,
                     limit: int = 100) -> CandidateRead:

        # If user hasn't permission to view all candidates, then return only supervised candidates
        if not self._check_by_role(db, role_id):
            return self._get_supervised_candidates(db, filter, user_id, skip, limit, CandidateStatusEnum.ACTIVE)

        return self._get_candidates_by_status(db, filter, skip, limit, CandidateStatusEnum.ACTIVE)

    def get_draft_candidates(self, db: Session,
                             filter: str,
                             user_id: str,
                             role_id: str,
                             skip: int = 0,
                             limit: int = 100) -> CandidateRead:

        # If user hasn't permission to view all candidates, then return only supervised draft candidates
        if not self._check_by_role(db, role_id):
            return self._get_supervised_candidates(db, filter, user_id, skip, limit, CandidateStatusEnum.DRAFT)

        return self._get_candidates_by_status(db, filter, skip, limit, CandidateStatusEnum.DRAFT)

    def get_by_id(self, db: Session, id: str):
        candidate = super().get_by_id(db, id)

        candidate = CandidateRead.from_orm(candidate).dict()

        self._validate_candidate(db, candidate)

        return candidate

    def create(self, db: Session, body: CandidateCreate):
        staff_unit_service.get_by_id(db, body.staff_unit_curator_id)
        staff_unit_service.get_by_id(db, body.staff_unit_id)
        candidate = super().create(db, body)
        
        stage_types = db.query(CandidateStageType).all()
        for stage_type in stage_types:
            candidate_stage_info = CandidateStageInfoCreate(
                candidate_id=candidate.id,
                candidate_stage_type_id=stage_type.id,
                staff_unit_coordinate_id=None,
                is_waits=False,
                status=CandidateStageInfoStatusEnum.NOT_STARTED.value
            )
            candidate_stage_info_service.create(db, candidate_stage_info)

        return candidate

    def update(self, db: Session, id: str, body: CandidateUpdate):

        candidate = super().get(db, id)

        if candidate is None:
            raise NotFoundException(detail=f"Candidate with id {id} not found!")

        if body.staff_unit_id is not None:
            staff_unit = staff_unit_service.get_by_id(db, body.staff_unit_id)
            candidate.staff_unit_id = staff_unit.id
        if body.staff_unit_curator_id is not None:
            staff_unit = staff_unit_service.get_by_id(db, body.staff_unit_curator_id)
            candidate.staff_unit_curator_id = staff_unit.id
        if body.status is not None:
            candidate.status = body.status

            if candidate.status == CandidateStatusEnum.DRAFT.value and body.debarment_reason is not None:
                candidate.debarment_reason = body.debarment_reason
            elif candidate.status == CandidateStatusEnum.ACTIVE.value:
                candidate.debarment_reason = None
        if body.is_physical_passed is not None:
            if body.is_physical_passed:
                candidate.is_physical_passed = body.is_physical_passed

        db.add(candidate)
        db.flush()

        return candidate

    def finish_candidate(self, db: Session, candidate_id: str, role: str):
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()

        current_user_staff_unit = staff_unit_service.get_by_id(db, role)

        if candidate.staff_unit_curator_id != current_user_staff_unit.id:
            raise ForbiddenException(
                detail=f"Вы не являетесь куратором кандидата: {candidate.id}"
            )

        stage_infos = db.query(CandidateStageInfo).filter(
            CandidateStageInfo.candidate_id == candidate.id
        ).all()

        for stage_info in stage_infos:
            if stage_info.status != CandidateStageInfoStatusEnum.APPROVED.value:
                raise BadRequestException(
                    detail=f"Кандидат: {candidate.id} не имеет право завершить изучение."
                )

        return "Кандидат: {candidate.id} завершил изучение!"

    def update_essay(self, db: Session, id: str, body: CandidateEssayUpdate):
        candidate = db.query(self.model).filter(self.model.id == id).first()

        if body.essay_id is not None:
            essay = candidate_essay_type_service.get_by_id(db, body.essay_id)
        else:
            essay = candidate_essay_type_service.create(db, CandidateEssayTypeCreate(
                name=body.name,
                nameKZ=body.nameKZ
            ))

            db.add(essay)

        candidate.essay_id = essay.id

        db.add(candidate)
        db.flush()

        return candidate

    # Check if user has permission to view all candidates
    def _check_by_role(self, db: Session, role_id: str) -> bool:
        staff_unit = staff_unit_service.get_by_id(db, role_id)

        available_all_roles = [position_service.get_by_name(db, name) for name in self.ALL_CANDIDATE_VIEWERS]

        return any(staff_unit.position_id == i for i in available_all_roles)

    def _validate_candidate(self, db: Session, candidate):
        candidate_stage_info_count = db.query(CandidateStageType).count()

        candidate_stage_info_success_count = db.query(
            CandidateStageInfo).filter(
            CandidateStageInfo.status == CandidateStageInfoStatusEnum.APPROVED.value,
            CandidateStageInfo.candidate_id == candidate['id']
        ).count()

        candidate[
            'progress'] = candidate_stage_info_success_count / candidate_stage_info_count * 100 if candidate_stage_info_count > 0 else 0

        current_stage_info = db.query(CandidateStageInfo).filter(
            CandidateStageInfo.status == CandidateStageInfoStatusEnum.PENDING.value,
            CandidateStageInfo.candidate_id == candidate['id']
        ).order_by(CandidateStageInfo.created_at.desc()).first()

        if current_stage_info:
            current_stage_type = db.query(CandidateStageType).filter(
                CandidateStageType.id == current_stage_info.candidate_stage_type_id
            ).first()

            if current_stage_type:
                candidate['current_stage'] = current_stage_type.name

        candidate_obj = super().get_by_id(db, candidate['id'])
        if candidate_obj.candidate_stage_answers:
            candidate['last_edit_date'] = candidate_obj.candidate_stage_answers[0].created_at

    def _get_candidates_by_status(self, db: Session,
                                  filter: str,
                                  skip: int = 0,
                                  limit: int = 100,
                                  status: CandidateStatusEnum = None) -> CandidateRead:

        if filter is not None:
            return self._get_candidates_by_status_and_filter(db, filter, skip, limit, status)

        return db.query(self.model).filter(
            self.model.status == status.value
        ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()

    def _get_candidates_by_status_and_filter(self, db: Session,
                                             filter: str,
                                             skip: int = 0,
                                             limit: int = 100,
                                             status: CandidateStatusEnum = None) -> CandidateRead:
        key_words = filter.lower().split()

        return (
            self._query_candidates(db, status, key_words)
            .order_by(self.model.id.asc())
            .offset(skip)
            .limit(limit)
            .all())

    def _get_supervised_candidates(self, db: Session,
                                   filter: str,
                                   user_id: str,
                                   skip: int = 0,
                                   limit: int = 100,
                                   status: CandidateStatusEnum = None) -> CandidateRead:
        user = user_service.get_by_id(db, user_id)

        if filter is not None:
            return self._get_supervised_candidates_by_status_and_filter(db, filter, user, skip, limit, status)

        return db.query(self.model).filter(
            self.model.staff_unit_curator_id == user.actual_staff_unit_id,
            self.model.status == status.value
        ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()

    def _get_supervised_candidates_by_status_and_filter(self, db: Session,
                                                        filter: str,
                                                        user: User,
                                                        skip: int = 0,
                                                        limit: int = 100,
                                                        status: CandidateStatusEnum = None) -> CandidateRead:
        key_words = filter.lower().split()

        return (
            self._query_candidates(db, status, key_words)
            .filter(user.actual_staff_unit_id == self.model.staff_unit_curator_id)
            .order_by(self.model.id.asc())
            .offset(skip)
            .limit(limit)
            .all())
    
    def _query_candidates(self, db: Session, status: CandidateStatusEnum, key_words: list[str]):
        return (
            db.query(self.model)
            .join(StaffUnit, self.model.staff_unit_id == StaffUnit.id)
            .join(User, User.staff_unit_id == StaffUnit.id)
            .filter(
                self.model.status == status.value,
                ((or_(*[func.lower(User.first_name).contains(name) for name in key_words])) |
                (or_(*[func.lower(User.last_name).contains(name) for name in key_words])) |
                (or_(*[func.lower(User.father_name).contains(name) for name in key_words])))
            )
        )


candidate_service = CandidateService(Candidate)  # type: ignore

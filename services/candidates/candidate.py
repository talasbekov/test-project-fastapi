from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import (Candidate, CandidateStageInfo, StaffUnit, User,
                    CandidateStatusEnum, Position, CandidateStageType,
                    PositionNameEnum, CandidateStageInfoStatusEnum, CandidateStageQuestion)
from schemas import CandidateCreate, CandidateUpdate, CandidateRead, CandidateStageInfoCreate, \
    CandidateStageAnswerCreate
from services import ServiceBase, staff_unit_service, user_service
from .candidate_essay_type import candidate_essay_type_service
from .candidate_stage_info import candidate_stage_info_service
from .candidate_stage_answer import candidate_stage_answer_service


class CandidateService(ServiceBase[Candidate, CandidateCreate, CandidateUpdate]):
    def get_multiple(self, db: Session, filter: str, user_id: str, role_id: str, skip: int = 0, limit: int = 100):

        if self._check_by_role(db, role_id):
            if filter is not None:
                filter = filter.lower()
                print(filter)
                candidates = db.query(self.model). \
                    join(StaffUnit, self.model.staff_unit_id == StaffUnit.id). \
                    join(User, User.staff_unit_id == StaffUnit.id). \
                    filter(self.model.status == CandidateStatusEnum.ACTIVE.value,
                           or_(func.lower(User.first_name).contains(filter),
                               func.lower(User.last_name).contains(filter),
                               func.lower(User.father_name).contains(filter))
                           ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()
            else:
                candidates = db.query(self.model).filter(
                    self.model.status == CandidateStatusEnum.ACTIVE.value
                ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()
        else:
            candidates = self._get_supervised_active_candidates(db, filter, user_id, skip, limit)

        candidates = [CandidateRead.from_orm(candidate).dict() for candidate in candidates]
        for candidate in candidates:
            self._validate_candidate(db, candidate)
        return candidates

    def get_draft_candidates(self, db: Session, filter: str, user_id: str, role_id: str, skip: int = 0,
                             limit: int = 100):

        if self._check_by_role(db, role_id):

            if filter is not None:
                candidates = db.query(self.model). \
                    join(StaffUnit, self.model.staff_unit_id == StaffUnit.id). \
                    join(User, User.staff_unit_id == StaffUnit.id). \
                    filter(
                    self.model.status == CandidateStatusEnum.DRAFT.value,
                    or_(func.lower(User.first_name).contains(filter),
                        func.lower(User.last_name).contains(filter),
                        func.lower(User.father_name).contains(filter))
                ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()
            else:
                candidates = db.query(self.model).filter(
                    self.model.status == CandidateStatusEnum.DRAFT.value,
                ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()
        else:
            candidates = self._get_supervised_draft_candidates(db, filter, user_id)

        candidates = [CandidateRead.from_orm(candidate).dict() for candidate in candidates]
        for candidate in candidates:
            self._validate_candidate(db, candidate)
        return candidates

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
                stage_type_id=stage_type.id,
                staff_unit_coordinate_id=None,
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
            PositionNameEnum.PERSONNEL_HEAD.value,
            PositionNameEnum.DEPUTY_PERSONNEL_HEAD.value,
            PositionNameEnum.CANDIDATE_MANAGEMENT_HEAD.value,
            PositionNameEnum.POLITICS_GOVERNMENT_SERVANT.value
        }

        available_all_roles = []

        for i in available_all:
            available_all_roles.append(self._get_role_by_name(db, i))

        for i in available_all_roles:
            if staff_unit.position_id == i:
                return True

        return False

    def _get_role_by_name(self, db: Session, name: str):
        role = db.query(Position).filter(
            Position.name == name
        ).first()

        if role:
            return role.id
        else:
            return None

    def _get_supervised_active_candidates(self, db: Session, filter: str, user_id: str, skip: int = 0,
                                          limit: int = 100):
        user = user_service.get_by_id(db, user_id)

        if filter is not None:
            filter = filter.lower()
            print(filter)
            return db.query(self.model). \
                join(StaffUnit, self.model.staff_unit_id == StaffUnit.id). \
                join(User, User.staff_unit_id == StaffUnit.id). \
                filter(
                self.model.staff_unit_curator_id == user.actual_staff_unit_id,
                self.model.status == CandidateStatusEnum.ACTIVE.value,
                or_(func.lower(User.first_name).contains(filter),
                    func.lower(User.last_name).contains(filter),
                    func.lower(User.father_name).contains(filter))
            ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()
        else:
            return db.query(self.model).filter(
                self.model.staff_unit_curator_id == user.actual_staff_unit_id,
                self.model.status == CandidateStatusEnum.ACTIVE.value
            ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()

    def _get_supervised_draft_candidates(self, db: Session, filter: str, user_id: str, skip: int = 0, limit: int = 100):
        user = user_service.get_by_id(db, user_id)

        if filter is not None:
            filter = filter.lower()
            return db.query(self.model). \
                join(StaffUnit, self.model.staff_unit_id == StaffUnit.id). \
                join(User, User.staff_unit_id == StaffUnit.id). \
                filter(
                self.model.staff_unit_curator_id == user.actual_staff_unit_id,
                self.model.status == CandidateStatusEnum.DRAFT.value,
                or_(func.lower(User.first_name).contains(filter),
                    func.lower(User.last_name).contains(filter),
                    func.lower(User.father_name).contains(filter))
            ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()
        else:
            return db.query(self.model).filter(
                self.model.staff_unit_curator_id == user.actual_staff_unit_id,
                self.model.status == CandidateStatusEnum.DRAFT.value
            ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()

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


candidate_service = CandidateService(Candidate)  # type: ignore

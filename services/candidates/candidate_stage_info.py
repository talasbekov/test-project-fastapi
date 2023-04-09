import uuid
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from exceptions import ForbiddenException, BadRequestException
from models import (CandidateStageInfo, Candidate, StaffUnit, User,
                    CandidateStageInfoStatusEnum, PositionNameEnum, Position, CandidateStageType)
from schemas import (CandidateStageInfoRead, CandidateStageInfoCreate, CandidateStageInfoUpdate,
                     CandidateStageInfoSendToApproval)
from services import ServiceBase, staff_unit_service
from .candidate_stage_type import candidate_stage_type_service


class CandidateStageInfoService(ServiceBase[CandidateStageInfo, CandidateStageInfoCreate, CandidateStageInfoUpdate]):

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ):
        return db.query(self.model).order_by(self.model.id.asc()).offset(skip).limit(limit).all()
    
    def get_all_by_staff_unit_id(self, db: Session, filter: str, skip: int, limit: int, staff_unit_id: str):

        if filter is not None:
            filter = filter.lower()
            candidates = db.query(CandidateStageInfo).\
                            join(Candidate, self.model.candidate_id == Candidate.id).\
                            join(StaffUnit, Candidate.staff_unit_id == StaffUnit.id).\
                            join(User, User.staff_unit_id == StaffUnit.id).\
                            filter(
                                CandidateStageInfo.staff_unit_coordinate_id == staff_unit_id,
                                CandidateStageInfo.is_waits == True,
                                or_(func.lower(User.first_name).contains(filter),
                                    func.lower(User.last_name).contains(filter),
                                    func.lower(User.father_name).contains(filter))
                            ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()
        else:
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

    def send_to_approval(self, db: Session, id: str, body: CandidateStageInfoSendToApproval, staff_unit_id: str):
        candidate_stage_info = super().get_by_id(db, id)

        current_user_staff_unit = staff_unit_service.get_by_id(db, staff_unit_id)

        candidate = db.query(Candidate).filter(
            Candidate.id == candidate_stage_info.candidate_id
        ).first()

        if candidate.staff_unit_curator_id != current_user_staff_unit.id:
            raise ForbiddenException(
                detail=f"Вы не являтеесь куратором для кандидата {candidate_stage_info.candidate_id}!"
            )

        if body.staff_unit_coordinate_id is not None:
            candidate_stage_info.staff_unit_coordinate_id = body.staff_unit_coordinate_id
        else:
            candidate_stage_info = self._send_to_multiple_approval(db, candidate_stage_info)

        candidate_stage_info.is_waits = True

        db.add(candidate_stage_info)
        db.flush()

        return candidate_stage_info

    def sign_candidate(self, db: Session, id: uuid.UUID, staff_unit_id: str):
        candidate_stage_info: CandidateStageInfo = super().get_by_id(db, id)

        self._validate_access(db, candidate_stage_info, staff_unit_id)

        candidate_stage_info.status = CandidateStageInfoStatusEnum.APPROVED.value
        candidate_stage_info.is_waits = False
        candidate_stage_info.date_sign = datetime.now()  # set the current date to the date_sign field

        db.add(candidate_stage_info)
        db.flush()

        return candidate_stage_info

    def reject_candidate(self, db: Session, id: uuid.UUID, staff_unit_id: str):
        candidate_stage_info: CandidateStageInfo = super().get_by_id(db, id)

        self._validate_access(db, candidate_stage_info, staff_unit_id)

        candidate_stage_info.status = CandidateStageInfoStatusEnum.DECLINED.value
        candidate_stage_info.is_waits = False
        candidate_stage_info.date_sign = datetime.now()  # set the current date to the date_sign field

        db.add(candidate_stage_info)
        db.flush()

        return candidate_stage_info

    def _validate_access(self, db: Session, candidate_stage_info: CandidateStageInfo, staff_unit_id: str):
        current_user_staff_unit = staff_unit_service.get_by_id(db, staff_unit_id)

        if not candidate_stage_info.is_waits or current_user_staff_unit.id != candidate_stage_info.staff_unit_coordinate_id:
            raise ForbiddenException(
                detail=f"У вас нет доступа к информации о стадии кандидата для CandidateStageInfo with id: {candidate_stage_info.id}!"
            )

    def _send_to_multiple_approval(self, db: Session, candidate_stage_info: CandidateStageInfo) -> CandidateStageInfo:
        candidate_stage_type = db.query(CandidateStageType).filter(
            CandidateStageType.id == candidate_stage_info.candidate_stage_type_id
        ).first()

        position = None

        if hasattr(candidate_stage_info, 'name'):
            if candidate_stage_type.name == 'Результаты полиграфологического исследования':
                position = self._get_role_by_name(db, PositionNameEnum.POLYGRAPH_EXAMINER.value)
            if candidate_stage_info.name == 'Результаты физической подготовки':
                position = self._get_role_by_name(db, PositionNameEnum.INSTRUCTOR.value)

        if position is None:
            raise BadRequestException(
                detail=f"Введите staff_unit_coordinate_id"
            )

        staff_unit = staff_unit_service.get_all_by_position(db, position.id)

        candidate_stage_info.staff_unit_coordinate_id = staff_unit.id

        return candidate_stage_info

    def _get_role_by_name(self, db: Session, name: str) -> Position:
        role = db.query(Position).filter(
            Position.name == name
        ).first()

        if role:
            return role.id
        else:
            return None


candidate_stage_info_service = CandidateStageInfoService(CandidateStageInfo) # type: ignore

from sqlalchemy import func, and_, desc
from sqlalchemy.orm import Session

from exceptions import NotFoundException, ForbiddenException, BadRequestException
from models import (Candidate, CandidateStageInfo, StaffUnit, User,
                    CandidateStatusEnum, CandidateStageType,
                    PositionNameEnum, CandidateStageInfoStatusEnum, StaffDivision)
from schemas import (
    CandidateCreate,
    CandidateUpdate,
    CandidateRead,
    CandidateStageInfoCreate,
    CandidateEssayUpdate,
    CandidateEssayTypeCreate
)
from services import ServiceBase, staff_unit_service, user_service, position_service
from .candidate_essay_type import candidate_essay_type_service
from .candidate_stage_info import candidate_stage_info_service


class CandidateService(
    ServiceBase[Candidate, CandidateCreate, CandidateUpdate]):
    # This const variable stores the positions which have access to all
    # candidates
    ALL_CANDIDATE_VIEWERS = {
        PositionNameEnum.PERSONNEL_HEAD.value,
        PositionNameEnum.DEPUTY_PERSONNEL_HEAD.value,
        PositionNameEnum.CANDIDATE_MANAGEMENT_HEAD.value,
        PositionNameEnum.POLITICS_GOVERNMENT_SERVANT.value,
        PositionNameEnum.HR.value
    }

    def get_all(self, db: Session):
        """
            Returns a list of all candidates.
        """
        return db.query(self.model).filter(
            self.model.status == CandidateStatusEnum.ACTIVE.value
        ).all()

    def get_all_by_staff_division(self,
                                  db: Session,
                                  staff_division: StaffDivision,
                                  status: str):
        """
            Returns a list of all candidates by curators within staff division.
        """
        candidates = (
            db.query(self.model)\
                .join(StaffUnit, self.model.staff_unit_curator_id == StaffUnit.id)\
                .filter(
                    self.model.status == status,
                    StaffUnit.staff_division_id == staff_division.id
                ).all()
        )
        for group in staff_division.children:
            candidates += self.get_all_by_staff_division(db, group, status)

        return candidates


    def get_count_completed_candidates(
            self, db: Session
    ):
        return db.query(self.model).filter(
            self.model.status == CandidateStatusEnum.COMPLETED.value
        ).count()

    def get_candidates_recursive(self, db: Session, department: StaffDivision):
        candidates = db.query(self.model) \
            .join(StaffUnit, self.model.staff_unit_id == StaffUnit.id) \
            .join(StaffDivision, StaffUnit.staff_division_id == StaffDivision.id) \
            .filter(
            self.model.status == CandidateStatusEnum.ACTIVE,
            self.model.staff_unit_id == StaffUnit.id,
            StaffUnit.staff_division_id == department.id
        ).all()

        # Recursively call this function for each child division
        for child in department.children:
            candidates.extend(self.get_candidates_recursive(db, child))
        return candidates

    def get_candidates_by_staff_division(self, db, department: StaffDivision):
        candidates = db.query(self.model) \
            .join(StaffUnit, self.model.staff_unit_curator_id == StaffUnit.id) \
            .join(StaffDivision, StaffUnit.staff_division_id == StaffDivision.id) \
            .filter(
            self.model.status == CandidateStatusEnum.ACTIVE,
            self.model.staff_unit_curator_id == StaffUnit.id,
            StaffUnit.staff_division_id == department.id
        ).order_by(desc(self.model.staff_unit_curator_id)).all()

        for child in department.children:
            candidates.extend(self.get_candidates_by_staff_division(db, child))
        return candidates

    def get_top_curators_by_candidates(self, db: Session, department: StaffDivision):

        candidates = self.get_candidates_by_staff_division(db, department)

        top_curators = {}
        for candidate in candidates:
            curator = user_service.get_user_by_staff_unit(
                db, candidate.staff_unit_curator_id
            )
            if curator.id in top_curators:
                top_curators[curator.id] += 1
            else:
                top_curators[curator.id] = 1
            if curator.id in top_curators:
                top_curators[curator.id] += 1
            else:
                top_curators[curator.id] = 1

        top_curators = {
            id: value for id, value in top_curators.items()
            if value is not None and value != ""
        }
        sorted_curators = sorted(top_curators.items(), key=lambda x: x[1], reverse=True)
        return sorted_curators

    def get_top_curator_duration_by_candidates(self,
                                               db: Session,
                                               department: StaffDivision):

        candidates = self.get_candidates_by_staff_division(db, department)

        top_curators = {}
        for candidate in candidates:
            curator = user_service.get_user_by_staff_unit(
                db, candidate.staff_unit_curator_id
            )
            if curator.id in top_curators:
                if candidate.created_at > top_curators[curator.id]:
                    top_curators[curator.id] = candidate.created_at
            else:
                top_curators[curator.id] = candidate.created_at


        top_curators = {
            id: value for id, value in top_curators.items()
            if value is not None and value != ""
        }
        sorted_curators = sorted(top_curators.items(), key=lambda x: x[1], reverse=True)
        return sorted_curators

    def get_multiple(self, db: Session,
                     filter: str,
                     user_id: str,
                     role_id: str,
                     skip: int = 0,
                     limit: int = 100) -> CandidateRead:
        """
            Returns a list of active candidates.

            If the user does not have permission to view all candidates,
            it returns only supervised candidates.
        """

        # If user hasn't permission to view all candidates, then return only
        # supervised candidates
        if not self._check_by_role(db, role_id):
            return self._get_supervised_candidates(
                db, filter, user_id, skip, limit, CandidateStatusEnum.ACTIVE)

        return self._get_candidates_by_status(
            db, filter, skip, limit, CandidateStatusEnum.ACTIVE)

    def get_draft_candidates(self, db: Session,
                             filter: str,
                             user_id: str,
                             role_id: str,
                             skip: int = 0,
                             limit: int = 100) -> CandidateRead:
        """
            Returns a list of draft candidates.

            If the user does not have permission to view all candidates,
            it returns only supervised draft candidates.
        """

        # If user hasn't permission to view all candidates, then return only
        # supervised draft candidates
        if not self._check_by_role(db, role_id):
            return self._get_supervised_candidates(
                db, filter, user_id, skip, limit, CandidateStatusEnum.DRAFT)

        return self._get_candidates_by_status(
            db, filter, skip, limit, CandidateStatusEnum.DRAFT)

    def get_by_id(self, db: Session, id: str):
        """
            Returns a single candidate based on the given ID.
        """
        candidate = super().get_by_id(db, id)

        return candidate

    def get_by_staff_unit_id(self, db: Session, staff_unit_id: str):
        """
            Returns a list of candidates based on the given staff unit ID.
        """
        candidates = db.query(Candidate).filter(
            Candidate.staff_unit_id == staff_unit_id).first()

        return candidates

    def create(self, db: Session, body: CandidateCreate):
        """
            Creates a new candidate and associated CandidateStageInfo
            objects for each stage type.
        """
        staff_unit_service.get_by_id(db, str(body.staff_unit_curator_id))
        staff_unit_service.get_by_id(db, str(body.staff_unit_id))
        candidate = super().create(db, body)

        stage_types = db.query(CandidateStageType).all()
        for stage_type in stage_types:
            candidate_stage_info = CandidateStageInfoCreate(
                candidate_id=str(candidate.id),
                candidate_stage_type_id=str(stage_type.id),
                staff_unit_coordinate_id=None,
                is_waits=False,
                status=CandidateStageInfoStatusEnum.NOT_STARTED.value
            )
            candidate_stage_info_service.create(db, candidate_stage_info)

        return candidate

    def update(self, db: Session, id: str, body: CandidateUpdate):

        candidate = super().get(db, id)

        if candidate is None:
            raise NotFoundException(
                detail=f"Candidate with id {id} not found!")

        if body.staff_unit_id is not None:
            staff_unit = staff_unit_service.get_by_id(db, body.staff_unit_id)
            candidate.staff_unit_id = staff_unit.id
        if body.staff_unit_curator_id is not None:
            staff_unit = staff_unit_service.get_by_id(
                db, body.staff_unit_curator_id)
            candidate.staff_unit_curator_id = staff_unit.id
        if body.status is not None:
            candidate.status = body.status

            if (candidate.status
                    == CandidateStatusEnum.DRAFT.value
                    and body.debarment_reason
                    is not None):
                candidate.debarment_reason = body.debarment_reason
            elif candidate.status == CandidateStatusEnum.ACTIVE.value:
                candidate.debarment_reason = None
        if body.is_physical_passed is not None:
            if body.is_physical_passed:
                candidate.is_physical_passed = body.is_physical_passed
        if body.recommended_by is not None:
            candidate.recommended_by = body.recommended_by

        db.add(candidate)
        db.flush()

        return candidate

    def finish_candidate(self, db: Session, candidate_id: str, role: str):
        """
            Finishes the review process for a candidate and
            raises exceptions
            if the user is not the candidate's curator or
            if the candidate has any pending stages
        """
        candidate = db.query(Candidate).filter(
            Candidate.id == candidate_id).first()

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
                    detail=(f"Кандидат: {candidate.id} "
                            "не имеет право завершить изучение.")
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

    def _check_by_role(self, db: Session, role_id: str) -> bool:
        """
            Checks if a user with the given role
            ID has permission to view all candidates.
        """
        staff_unit = staff_unit_service.get_by_id(db, role_id)

        available_all_roles = [position_service.get_id_by_name(
            db, name) for name in self.ALL_CANDIDATE_VIEWERS]

        return any(staff_unit.position_id == i for i in available_all_roles)

    def _validate_candidate(self, db: Session, candidate):
        """
            Validates a candidate's progress and
            sets additional properties on the candidate object.
        """
        candidate_stage_info_count = db.query(CandidateStageType).count()
        candidate['id'] = str(candidate['id'])
        
        candidate_stage_info_success_count = db.query(
            CandidateStageInfo).filter(
            CandidateStageInfo.status == CandidateStageInfoStatusEnum.APPROVED.value,
            CandidateStageInfo.candidate_id == candidate['id']
        ).count()

        candidate['progress'] = (
            candidate_stage_info_success_count
            / candidate_stage_info_count
            * 100
            if candidate_stage_info_count > 0
            else 0
        )

        current_stage_info = db.query(CandidateStageInfo).filter(
            CandidateStageInfo.status == CandidateStageInfoStatusEnum.PENDING.value,
            CandidateStageInfo.candidate_id == candidate['id']
        ).order_by(CandidateStageInfo.date_sign.desc()).first()

        if not current_stage_info:
            current_stage_info = db.query(CandidateStageInfo).filter(
                CandidateStageInfo.status
                == CandidateStageInfoStatusEnum.APPROVED.value,
                CandidateStageInfo.candidate_id == candidate['id']
            ).order_by(CandidateStageInfo.date_sign.desc()).first()

        if current_stage_info:
            current_stage_type = db.query(CandidateStageType).filter(
                CandidateStageType.id == current_stage_info.candidate_stage_type_id
            ).first()

            if current_stage_type:
                candidate['current_stage'] = current_stage_type.name

        candidate_obj = super().get_by_id(db, candidate['id'])
        if candidate_obj.candidate_stage_answers:
            candidate['last_edit_date'] = \
                candidate_obj.candidate_stage_answers[0].created_at

    def _get_candidates_by_status(self, db: Session,
                                  filter: str,
                                  skip: int = 0,
                                  limit: int = 100,
                                  status: CandidateStatusEnum = None) -> CandidateRead:
        """
            Returns a list of candidates based on the given status and filter.
        """
        filter.lstrip().rstrip()
        if filter != '':
            candidates = self._get_candidates_by_status_and_filter(
                db, filter, skip, limit, status)
        else:
            candidates = db.query(self.model).filter(
                self.model.status == status.value
            ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()

        candidates = [CandidateRead.from_orm(
            candidate).dict() for candidate in candidates]

        for candidate in candidates:
            self._validate_candidate(db, candidate)

        return candidates

    def _get_candidates_by_status_and_filter(self, db: Session,
                                filter: str,
                                skip: int = 0,
                                limit: int = 100,
                                status: CandidateStatusEnum = None) -> CandidateRead:
        """
            Returns a list of candidates based on the given status
            and filtered by the given keyword.
        """
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
                                   status: CandidateStatusEnum = None
                                   ) -> CandidateRead:
        """
            Returns a list of supervised candidates.

            If the user does not have permission to view all candidates,
            it returns only supervised candidate
        """
        user = user_service.get_by_id(db, user_id)

        if filter != '':
            candidates = self._get_supervised_candidates_by_status_and_filter(
                db, filter, user, skip, limit, status)
        else:
            candidates = db.query(self.model).filter(
                self.model.staff_unit_curator_id == user.staff_unit_id,
                self.model.status == status.value
            ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()

        candidates = [CandidateRead.from_orm(
            candidate).dict() for candidate in candidates]

        for candidate in candidates:
            self._validate_candidate(db, candidate)

        return candidates

    def _get_supervised_candidates_by_status_and_filter(self, db: Session,
                                                        filter: str,
                                                        user: User,
                                                        skip: int = 0,
                                                        limit: int = 100,
                                                        status:
                                                        CandidateStatusEnum = None
                                                        ) -> CandidateRead:
        """
            Returns a list of supervised candidates based on the given status
            and filtered by the given keyword.
        """
        key_words = filter.lower().split()

        return (
            self._query_candidates(db, status, key_words)
            .filter(user.staff_unit_id == self.model.staff_unit_curator_id)
            .order_by(self.model.id.asc())
            .offset(skip)
            .limit(limit)
            .all())

    def _query_candidates(
            self, db: Session, status: CandidateStatusEnum, key_words: list[str]):
        """
            Performs a query on the Candidate model and returns
            a filtered query based on the given status and filter.
        """
        return (
            db.query(self.model)
            .join(StaffUnit, self.model.staff_unit_id == StaffUnit.id)
            .join(User, User.staff_unit_id == StaffUnit.id)
            .filter(
                self.model.status == status.value
            )
            .filter(
                and_(func.concat(func.lower(User.first_name), ' ',
                                 func.lower(User.last_name), ' ',
                                 func.lower(User.father_name)).contains(name)
                     for name in key_words)
            )
        )


candidate_service = CandidateService(Candidate)  # type: ignore

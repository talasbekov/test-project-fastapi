import uuid
from datetime import datetime

import requests
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from core import configs
from exceptions import ForbiddenException, BadRequestException
from models import (
    CandidateStageInfo,
    Candidate,
    StaffUnit,
    User,
    CandidateStageInfoStatusEnum,
    PositionNameEnum,
    CandidateStageType
)
from models.association import s_u_cand_stage_infos
from schemas import (
    CandidateStageInfoRead,
    CandidateStageInfoCreate,
    CandidateStageInfoUpdate,
    CandidateStageInfoSendToApproval, CandidateStageInfoSignEcp
)
from services import ServiceBase, staff_unit_service, position_service
from .candidate_stage_type import candidate_stage_type_service


class CandidateStageInfoService(
        ServiceBase[CandidateStageInfo,
                    CandidateStageInfoCreate,
                    CandidateStageInfoUpdate]):

    def get_all_by_staff_unit_id(
            self,
            db: Session,
            filter: str,
            skip: int,
            limit: int,
            staff_unit_id: str) -> CandidateStageInfoRead:
        """
            Retrieves a list of CandidateStageInfo records for a specific staff_unit_id.
        """
        candidate_stage_info_id = \
            s_u_cand_stage_infos.c.candidate_stage_info_id
        staff_unit_candidate_id = s_u_cand_stage_infos.c.staff_unit_id
        if filter == '':
            subquery = (db
                        .query(candidate_stage_info_id)
                        .filter(staff_unit_candidate_id == staff_unit_id)
            )
            return db.query(CandidateStageInfo).filter(
                CandidateStageInfo.id.in_(subquery),
                CandidateStageInfo.is_waits == 1
            ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()

        key_words = filter.lower().split()

        return (
            self._query_candidate_stage_infos(db, staff_unit_id, key_words)
            .order_by(self.model.id.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_by_candidate_id(
            self, db: Session, skip: int, limit: int, candidate_id: str, role: str):
        """
            Retrieves a list of CandidateStageInfo records for a specific candidate_id.

            It also validates the candidate by calling
            the _validate_candidate_infos method.
        """
        candidate_stage_infos = db.query(CandidateStageInfo).filter(
            CandidateStageInfo.candidate_id == candidate_id,
        ).order_by(self.model.id.asc()).offset(skip).limit(limit).all()

        candidate_stage_infos = [CandidateStageInfoRead.from_orm(
            candidate_stage_info).dict()
            for candidate_stage_info in candidate_stage_infos]

        current_user_staff_unit = staff_unit_service.get_by_id(db, role)

        candidate = db.query(Candidate).filter(
            Candidate.id == candidate_id).first()

        for candidate_stage_info in candidate_stage_infos:
            self._validate_candidate_infos(
                db,
                candidate_stage_info=candidate_stage_info,
                candidate=candidate,
                current_user_staff_unit=current_user_staff_unit)

        return candidate_stage_infos

    def send_to_approval(self,
                         db: Session,
                         id: str,
                         body: CandidateStageInfoSendToApproval,
                         staff_unit_id: str):
        """
            Sends a CandidateStageInfo record to approval.

            This updates a CandidateStageInfo record's is_waits flag to True,
            indicating that it is waiting for approval.
            If a staff_unit_coordinate_id is provided, it sets it
            as the coordinator unit for the CandidateStageInfo.
            Otherwise, it sends the CandidateStageInfo to multiple approvers
            based on the type of the CandidateStageInfo and sets
            the staff_unit_coordinate_id accordingly.
        """
        candidate_stage_info = super().get_by_id(db, id)

        current_user_staff_unit = staff_unit_service.get_by_id(
            db, staff_unit_id)

        candidate = db.query(Candidate).filter(
            Candidate.id == candidate_stage_info.candidate_id
        ).first()

        if candidate.staff_unit_curator_id != current_user_staff_unit.id:
            raise ForbiddenException(
                detail=("Вы не являтеесь куратором"
                        f" для кандидата {candidate_stage_info.candidate_id}!")
            )

        if body.staff_unit_coordinate_id is not None:
            staff_unit = staff_unit_service.get_by_id(db,
                                body.staff_unit_coordinate_id
            )

            candidate_stage_info.staff_unit_coordinate_ids.append(staff_unit)
        else:
            candidate_stage_info = self._send_to_multiple_approval(
                db, candidate_stage_info, candidate)

        candidate_stage_info.is_waits = True

        db.add(candidate_stage_info)
        db.flush()

        return candidate_stage_info

    def sign_candidate_info(self, db: Session, id: str, role: str):
        """
            This method updates the CandidateStageInfo record with the provided
            id and sets its status to APPROVED.

            If the CandidateStageInfo is related to physical training results,
            it also updates the related Candidate record
                and sets its is_physical_passed flag to True.
        """
        candidate_stage_info: CandidateStageInfo = super().get_by_id(db, id)

        # self._validate_access_to_candidate_info(db, candidate_stage_info, role)

        candidate_stage_type = candidate_stage_type_service.get_by_id(
            db, candidate_stage_info.candidate_stage_type_id)

        if candidate_stage_type.name == "Результаты физической подготовки":
            candidate = db.query(Candidate).filter(
                Candidate.id == candidate_stage_info.candidate_id
            ).first()

            candidate.is_physical_passed = True

            db.add(candidate)

        candidate_stage_info.status = CandidateStageInfoStatusEnum.APPROVED.value
        candidate_stage_info.is_waits = False
        # set the current date to the date_sign field
        candidate_stage_info.date_sign = datetime.now()

        db.add(candidate_stage_info)
        db.flush()

        return candidate_stage_info

    async def sign_with_certificate(self,
                                    db: Session,
                                    id: str,
                                    body: CandidateStageInfoSignEcp,
                                    access_token,
                                    role,
                                    user_id):
        candidate_stage_info = self.sign_candidate_info(db, id, role)

        url = configs.ECP_SERVICE_URL + 'api/candidate_stage_signer/create/'
        request_body = {
            'candidates_stage_id': str(id),
            'user_id': str(user_id),
            'certificate_blob': body.certificate_blob,
            'xml_sign': None
        }
        headers = {"Authorization": f"Bearer {access_token}"}

        res = requests.post(url=url, json=request_body, headers=headers)

        if res.status_code >= 400:
            raise BadRequestException(detail=res.text)

        return candidate_stage_info

    def reject_candidate_info(self, db: Session, id: str, role: str):
        """
            This updates the CandidateStageInfo record with the provided id
            and sets its status to DECLINED.
            If the CandidateStageInfo is related to physical training results,
            it also updates the related Candidate
            record and increments its attempt_number
        """
        candidate_stage_info: CandidateStageInfo = super().get_by_id(db, id)

        # self._validate_access_to_candidate_info(db, candidate_stage_info, role)

        candidate_stage_type = candidate_stage_type_service.get_by_id(
            db, candidate_stage_info.candidate_stage_type_id)

        if candidate_stage_type.name == "Результаты физической подготовки":
            candidate = db.query(Candidate).filter(
                Candidate.id == candidate_stage_info.candidate_id
            ).first()

            if candidate.attempt_number == 2:
                candidate.is_physical_passed = False
            else:
                candidate.is_physical_passed = None
                candidate.attempt_number += 1

            db.add(candidate)

        candidate_stage_info.status = CandidateStageInfoStatusEnum.DECLINED.value
        candidate_stage_info.is_waits = False
        # set the current date to the date_sign field
        candidate_stage_info.date_sign = datetime.now()

        db.add(candidate_stage_info)
        db.flush()

        return candidate_stage_info

    def _validate_access_to_candidate_info(
            self, db: Session, candidate_stage_info: CandidateStageInfo, role: str):
        """
            This method validates whether the current user
            has access to the CandidateStageInfo record with the provided id.
        """
        current_user_staff_unit = staff_unit_service.get_by_id(db, role)

        if (not candidate_stage_info.is_waits
            or current_user_staff_unit.id
            != candidate_stage_info.staff_unit_coordinate_id):
            raise ForbiddenException(
                detail=("У вас нет доступа к информации о стадии"
        f" кандидата для CandidateStageInfo with id: {candidate_stage_info.id}!")
            )

    def _send_to_multiple_approval(
            self,
            db: Session,
            candidate_stage_info: CandidateStageInfo,
            candidate) -> CandidateStageInfo:
        """
            This method sends the CandidateStageInfo to multiple approvers
            based on the type of the CandidateStageInfo and sets
            the staff_unit_coordinate_id accordingly.
        """
        candidate_stage_type = db.query(CandidateStageType).filter(
            CandidateStageType.id == candidate_stage_info.candidate_stage_type_id
        ).first()

        position = None

        if candidate_stage_type.name == 'Результаты полиграфологического исследования':
            position = position_service.get_id_by_name(
                db, PositionNameEnum.POLYGRAPH_EXAMINER.value)
        if candidate_stage_type.name == 'Результаты физической подготовки':
            position = position_service.get_id_by_name(
                db, PositionNameEnum.INSTRUCTOR.value)

            if candidate.attempt_number >= 2:
                raise BadRequestException(
                    detail=("Кандидат имеет только два шанса"
                            " для прохождения физической подготовки!")
                )

        if position is None:
            raise BadRequestException(
                detail="Введите staff_unit_coordinate_id"
            )

        staff_units = staff_unit_service.get_all_by_position(db, position)

        for staff_unit in staff_units:
            candidate_stage_info.staff_unit_coordinate_ids.append(staff_unit)

        db.add(candidate_stage_info)
        db.flush()

        return candidate_stage_info

    def _validate_candidate_infos(self,
                                  db: Session,
                                  candidate_stage_info: CandidateStageInfo,
                                  candidate,
                                  current_user_staff_unit):
        """
            This method validates whether the current user
            has access to the CandidateStageInfo record with the provided id.
        """

        if candidate.staff_unit_curator_id == current_user_staff_unit.id:
            candidate_stage_info['access'] = True

            return candidate_stage_info

        position = position_service.get_by_id(
            db, current_user_staff_unit.position_id)

        candidate_stage_type = candidate_stage_type_service.get_by_id(
            db, candidate_stage_info['candidate_stage_type_id'])

        if position.name == PositionNameEnum.PSYCHOLOGIST.value:
            if candidate_stage_type.name == 'Беседа с психологом':
                candidate_stage_info['access'] = True
            else:
                candidate_stage_info['access'] = False
        if (position.name
            == PositionNameEnum.REPRESENTATIVE_OF_SECURITY_DEPARTMENT.value):
            if candidate_stage_type.name == 'Беседа с представителем УСБ':
                candidate_stage_info['access'] = True
            else:
                candidate_stage_info['access'] = False
        if position.name == PositionNameEnum.POLYGRAPH_EXAMINER.value:
            if (candidate_stage_type.name
                == 'Результаты полиграфологического исследования'):
                candidate_stage_info['access'] = True
            else:
                candidate_stage_info['access'] = False

    def _query_candidate_stage_infos(
            self, db: Session, staff_unit_id: str, key_words: list[str]):
        """
            This method returns the query for getting the CandidateStageInfo
            records based on the provided staff_unit_id and key_words.
        """
        candidate_stage_info_id = \
            s_u_cand_stage_infos.c.candidate_stage_info_id
        staff_unit_candidate_id = \
            s_u_cand_stage_infos.c.staff_unit_id
        subquery = (db
                    .query(candidate_stage_info_id)
                    .filter(staff_unit_candidate_id
                            == staff_unit_id)
        )

        return (
            db.query(CandidateStageInfo)
            .join(Candidate, self.model.candidate_id == Candidate.id)
            .join(StaffUnit, Candidate.staff_unit_id == StaffUnit.id)
            .join(User, User.staff_unit_id == StaffUnit.id)
            .filter(
                CandidateStageInfo.id.in_(subquery),
                CandidateStageInfo.is_waits == True,
                (and_(func.concat(func.lower(User.first_name), ' ',
                        func.lower(User.last_name), ' ',
                        func.lower(User.father_name)).contains(name)
                        for name in key_words))
            )
        )
        
    def get_count_passed_stages(self, db: Session, candidate_id: str):
        """
            This method returns the count of passed stages
            for the Candidate with the provided id.
        """
        return (
            db.query(CandidateStageInfo)
            .filter(
                CandidateStageInfo.candidate_id == candidate_id,
                CandidateStageInfo.status == CandidateStageInfoStatusEnum.APPROVED.value
            )
            .count()
        )


candidate_stage_info_service = CandidateStageInfoService(
    CandidateStageInfo)  # type: ignore

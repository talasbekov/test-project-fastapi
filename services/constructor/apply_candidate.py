import datetime

from sqlalchemy.orm import Session

from core import configs
from models import (User, ContractType, ContractHistory, 
                    HrDocument, StaffDivisionEnum, CandidateStatusEnum,
                    EmergencyServiceHistory, Rank)
from .base import BaseHandler
from services import (contract_service, history_service, 
                      staff_division_service, staff_unit_service)
from services.candidates import candidate_service
from exceptions import NotFoundException, BadRequestException


def get_last_by_user_id(db: Session, user_id: str):
    res = (
        db.query(ContractHistory)
        .filter(ContractHistory.user_id == user_id)
        .order_by(ContractHistory.date_to.desc())
        .first()
    )
    return res


class ApplyCandidateHandler(BaseHandler):
    __handler__ = "apply_candidate"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):

        self.handle_validation(
            db, user, action, template_props, props, document)

        (contract_type,
            date_from,
            date_to,
            new_position,
            new_rank) = self.get_args(db, action, props)

        candidate = candidate_service.get_by_staff_unit_id(db, user.staff_unit_id)
        candidate.status = CandidateStatusEnum.COMPLETED.value
        db.add(candidate)
        
        position_old_history = staff_unit_service.get_last_history(db, user.id)
        
        if position_old_history is None:
            staff_unit = user.staff_unit
            position_history: EmergencyServiceHistory = history_service.create_history(
                db, user.id, staff_unit)
            position_old_history = staff_unit_service.get_last_history(db, user.id)
            
        user.rank_id = new_rank.id

        res = staff_unit_service.create_relation(db, user, new_position)

        position_history: EmergencyServiceHistory = history_service.create_history(
            db, user.id, res)
        position_history.document_link = configs.GENERATE_IP + str(document.id)
        db.add(position_history)
        
        res = contract_service.create_relation(db, user.id, contract_type.id)
        user.contracts.append(res)
        if contract_type.is_finite:
            contract_history = history_service.create_timeline_history(
                db, user.id, res, date_from, date_to
            )
        else:
            contract_history = history_service.create_history(db, user.id, res)
        contract_history.document_link = configs.GENERATE_IP + str(document.id)

        db.add(user)
        db.add(document)
        db.add(contract_history)
        db.flush()

        return user

    def handle_validation(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        try:
            candidate_staff_division = (
            staff_division_service.get_by_name(
                db, StaffDivisionEnum.CANDIDATES.value)
        )
            if user.staff_unit.staff_division_id != candidate_staff_division.id:
                raise BadRequestException(
                    detail=f'Invalid props for action: {self.__handler__}')
        except Exception:
            raise BadRequestException(
                detail=f'Invalid props for action: {self.__handler__}')

    def get_args(
            self,
            db: Session,
            action: dict,
            props: dict,
    ):
        try:
            contract_type_id = props[action["contract"]["tagname"]]["value"]
            contract_type = db.query(ContractType).filter(
                ContractType.id == contract_type_id
            ).first()

            if not contract_type:
                raise NotFoundException(
                    detail="Contract type not found"
                )
            date_from = datetime.datetime.now()
            date_to = date_from.replace(date_from.year + contract_type.years)
        except Exception:
            raise BadRequestException(
                detail=f'Invalid props for action: {self.__handler__}')
        try:
            position_id = props[action["staff_unit"]["tagname"]]["value"]
        except KeyError:
            raise BadRequestException(
                f"Position is not defined for this action: {self.__handler__}")
        try:
            rank_id = props[action["rank"]["tagname"]]["value"]
            rank = db.query(Rank).filter(
                Rank.id == rank_id
            ).first()
        except Exception:
            raise BadRequestException(
                detail=f'Invalid props for action: {self.__handler__}')
        return contract_type, date_from, date_to, position_id, rank

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        data = list(self.get_args(db, action, properties))
        return data


handler = ApplyCandidateHandler()

import logging
import json

from sqlalchemy.orm import Session

from core import configs
from models import (User, HrDocument, EmergencyServiceHistory,
                    StaffDivisionEnum, CandidateStatusEnum)
from schemas import StaffUnitRead
from .base import BaseHandler
from services import (staff_unit_service, history_service,
                      staff_division_service)
from services.candidates import candidate_service
from exceptions import BadRequestException


class PositionChangeHandler(BaseHandler):
    __handler__ = "position_change"

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
        
        candidate_staff_division = (
            staff_division_service.get_by_name(
                db, StaffDivisionEnum.CANDIDATES.value)
        )
        
        if user.staff_unit.staff_division_id == candidate_staff_division.id:
            candidate = candidate_service.get_by_staff_unit_id(db, user.staff_unit_id)
            
            position_id = self.get_args(action, props)[0]
            
            percent = None
            reason = None
            
            candidate.status = CandidateStatusEnum.COMPLETED.value
            
            db.add(candidate)
        else:
            position_id, percent, reason = self.get_args(action, props)
        
        old_history = staff_unit_service.get_last_history(db, user.id)

        if old_history is None:
            staff_unit = user.staff_unit
            history: EmergencyServiceHistory = history_service.create_history(
                db, user.id, staff_unit)
            old_history = staff_unit_service.get_last_history(db, user.id)

        res = staff_unit_service.create_relation(db, user, position_id)
        history: EmergencyServiceHistory = history_service.create_history(
            db, user.id, res)
        history.percentage = percent
        history.reason = reason
        history.document_link = configs.GENERATE_IP + str(document.id)

        document.old_history_id = old_history.id
        
        db.add(user)
        db.add(history)
        db.add(document)

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
        candidate_staff_division = (
            staff_division_service.get_by_name(
                db, StaffDivisionEnum.CANDIDATES.value)
        )
        if isinstance(candidate_staff_division.description, str):
            candidate_staff_division.description = json.dumps(candidate_staff_division.description)
        position_id = self.get_args(action, props)[0]
        if isinstance(user.staff_unit.staff_division.description, str):
            user.staff_unit.staff_division.description = json.dumps(user.staff_unit.staff_division.description)

        if user.staff_unit.staff_division_id != candidate_staff_division.id:
            percent = self.get_args(action, props)[1]

            staff_unit_service.get_by_id(db, position_id)
            
            if percent < 0 or percent > 100:
                raise BadRequestException(
                    f"Percentage must be between 0 and 100: {percent}")
        
        if staff_unit_service.exists_relation(db, user.id, position_id):
            raise BadRequestException(
                ("This position is already assigned to this user:"
                f" {user.first_name}, {user.last_name}")
            )

    def get_args(self, action, properties):
        try:
            position_id = properties[action["staff_unit"]["tagname"]]["value"]
        except KeyError as e:
            logging.exception(e)
            raise BadRequestException(
                f"Position is not defined for this action: {self.__handler__}")
        try:
           percent = int(properties[action["percent"]["tagname"]]["name"])
        except KeyError as e:
            logging.exception(e)
            raise BadRequestException(
                f"Percent is not defined for this action: {self.__handler__}")
        try:
           reason = properties[action["reason"]["tagname"]]["name"]
        except KeyError as e:
            logging.exception(e)
            raise BadRequestException(
                f"Reason is not defined for this action: {self.__handler__}")
        return position_id, percent, reason

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        args, _, _ = self.get_args(action, properties)
        obj = staff_unit_service.get_by_id(db, args)
        if isinstance(obj.requirements, str):
            obj.requirements = json.loads(obj.requirements)
        if isinstance(obj.staff_division.description, str):
            obj.staff_division.description = json.loads(obj.staff_division.description)
        return StaffUnitRead.from_orm(obj)


handler = PositionChangeHandler()

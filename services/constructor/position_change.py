import logging
import json

from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from core import configs
from models import (User, HrDocument, EmergencyServiceHistory)
from schemas import ShortUserStaffUnitRead
from .base import BaseHandler
from services import (staff_unit_service, history_service,
                      history_service)

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
        position_id, percent, reason = self.get_args(action, props)
        old_history = staff_unit_service.get_last_history(db, user.id)

        if old_history is None:
            staff_unit = user.staff_unit
            if isinstance(staff_unit.staff_division.description, dict):
                staff_unit.staff_division.description = json.dumps(
                    staff_unit.staff_division.description)
            history: EmergencyServiceHistory = history_service.create_history(
                db, user.id, staff_unit)
            old_history = staff_unit_service.get_last_history(db, user.id)

        res = staff_unit_service.create_relation(db, user, position_id)
        if isinstance(res.staff_division.description, dict):
            res.staff_division.description = json.dumps(
                res.staff_division.description)
        if isinstance(res.requirements, list):
            res.requirements = json.dumps(res.requirements)

        history: EmergencyServiceHistory = history_service.create_history(
            db, user.id, res)
        history.percentage = percent
        history.reason = reason
        history.document_link = configs.GENERATE_IP + str(document.id)

        document.old_history_id = old_history.id
        if isinstance(user.staff_unit.staff_division.description, dict):
            user.staff_unit.staff_division.description = json.dumps(
                user.staff_unit.staff_division.description)
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
        if history_service.has_penalty_history(db, user.id):
            raise BadRequestException(
                f"Инициирование приказа возможно после снятия взыскания!")

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
            obj.staff_division.description = json.loads(
                obj.staff_division.description)
        return ShortUserStaffUnitRead.from_orm(obj)


handler = PositionChangeHandler()

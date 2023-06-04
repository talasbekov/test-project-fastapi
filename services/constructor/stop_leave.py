from datetime import datetime

from typing import Any
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, Query

from core import configs
from models import User, HrDocument, StatusEnum, StatusHistory, Status
from services import status_service, history_service
from exceptions import ForbiddenException
from utils import convert_str_to_datetime
from .base import BaseHandler


class StopLeaveHandler(BaseHandler):
    __handler__ = "stop_leave"

    def handle_action(
            self,
            db: Session,
            user: User,
            action: dict,
            template_props: dict,
            props: dict,
            document: HrDocument,
    ):
        reason = self.get_args(props, action)

        self.handle_validation(db, user, action, template_props, props, document)

        statuses = status_service.get_active_status_of_user(db, user.id, StatusEnum.ROOT.value)
        status = statuses[0]
        if status is None:
            return
        res = status_service.stop_relation(db, user.id, status.id)
        res.cancel_document_link = configs.GENERATE_IP + str(document.id)
        db.flush()

    def handle_validation(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        pass

    def get_args(
            self,
            props: dict,
            action: dict
    ):
        try:
            reason = props[action['reason']['tagname']]['name']
        except:
            raise ForbiddenException(detail=f'Invalid props for action: {self.__handler__}')
        return (reason)

    def handle_filter(self, db: Session, query: Query[Any]):
        statuses = [i.id for i in status_service.get_by_name(db, StatusEnum.ROOT.value)]
        return (
            query
            .join(
                Status,
                and_(
                    Status.user_id == User.id,
                    Status.type_id.in_(statuses),
                )
            )
            .join(
                StatusHistory,
                and_(
                    Status.id == StatusHistory.status_id,
                    or_(
                        StatusHistory.date_to == None,
                        StatusHistory.date_to > datetime.now(),
                    ),
                ),
            )
        )

    def handle_response(self, db: Session,
                        action: dict,
                        properties: dict,
                        ):
        return None


handler = StopLeaveHandler()

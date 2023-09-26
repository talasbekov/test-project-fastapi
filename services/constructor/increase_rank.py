from typing import Any

from sqlalchemy.orm import Session, Query, aliased

from core import configs
from models import User, HrDocument, Rank, Position, StaffUnit
from .base import BaseHandler
from services import rank_service, history_service
from exceptions import ForbiddenException, BadRequestException


class IncreaseRankHandler(BaseHandler):
    __handler__ = "increase_rank"

    def handle_action(
            self,
            db: Session,
            user: User,
            action: dict,
            template_props: dict,
            props: dict,
            document: HrDocument,
    ):
        rank_id = self.get_args(action, props)
        rank = rank_service.get_by_id(db, rank_id)

        self.handle_validation(
            db, user, action, template_props, props, document)
        user.rank = rank
        history = rank_service.find_last_history(db, user.id)
        res = history_service.create_history(db, user.id, rank)
        document.old_history = history
        res.document_link = configs.GENERATE_IP + str(document.id)
        db.add(user)
        db.add(res)
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
        rank_id = self.get_args(action, props)
        rank = rank_service.get_by_id(db, rank_id)
        user_rank = rank_service.get_by_id(db, user.rank_id)

        if user_rank.rank_order >= rank.rank_order:
            raise ForbiddenException(
                detail=f"You can not increase rank to {rank.name}")
        if history_service.has_penalty_history(db, user.id):
            raise BadRequestException(
                f"Инициирование приказа возможно после снятия взыскания!")

    def handle_filter(self, db: Session, user_query: Query[Any]):
        max_rank = rank_service.get_max_rank(db)
        position_rank = aliased(Rank)
        user_rank = aliased(Rank)
        return (
            user_query.filter(User.rank_id != max_rank.id)
            .join(StaffUnit, User.staff_unit_id == StaffUnit.id)
            .join(Position, StaffUnit.position_id == Position.id)
            .join(Position.max_rank.of_type(position_rank))
            .join(User.rank.of_type(user_rank))
            .filter(position_rank.rank_order > user_rank.rank_order)
        )

    def get_args(self, action, properties):
        try:
            rank_id = properties[action["rank"]["tagname"]]["value"]
        except KeyError:
            raise BadRequestException(
                f"Rank is not defined for this action: {self.__handler__}")
        return rank_id

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        args = self.get_args(action, properties)
        obj = rank_service.get_by_id(db, args)
        return obj


handler = IncreaseRankHandler()

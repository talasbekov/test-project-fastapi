from typing import Any

from sqlalchemy.orm import Session, Query

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import rank_service, history_service
from exceptions import ForbiddenException


class DecreaseRankHandler(BaseHandler):
    __handler__ = "decrease_rank"

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
        self.handle_validation(db, user, action, props)
        user.rank = rank
        history = rank_service.find_last_history(db, user.id)
        res = history_service.create_history(db, user.id, rank)
        res.document_link = configs.GENERATE_IP + str(document.id)
        document.old_history = history
        db.add(user)
        db.add(document)
        db.add(res)
        db.flush()

        return user
    
    def handle_validation(
        self,
        db: Session,
        user: User,
        action: dict,
        props: dict,
    ):
        rank_id = self.get_args(action, props)
        rank = rank_service.get_by_id(db, rank_id)
        if user.rank.order <= rank.order:
            raise ForbiddenException(detail=f"You can not decrease rank to {rank.name}")

    def handle_filter(self, db: Session, user_query: Query[Any]):
        min_rank = rank_service.get_min_rank(db)
        return user_query.filter(User.rank_id != min_rank.id)

    def get_args(self, action, properties):
        try:
            rank_id = properties[action["rank"]["tagname"]]["value"]
        except KeyError:
            raise ForbiddenException(f"Rank is not defined for this action: {self.__handler__}")
        return rank_id

    def handle_response(self, db: Session,
                        action: dict,
                        properties: dict,
                        ):
        args = self.get_args(action, properties)
        obj = rank_service.get_by_id(db, args)
        return obj


handler = DecreaseRankHandler()

from typing import Any

from sqlalchemy.orm import Session, Query

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import rank_service, history_service
from exceptions import ForbiddenException


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
        tagname = action["rank"]["tagname"]
        rank = rank_service.get_by_id(db, props[tagname]["value"])

        self.handle_validation(db, user, action, template_props, props, document)
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
        tagname = action["rank"]["tagname"]
        rank = rank_service.get_by_id(db, props[tagname]["value"])
        user_rank = rank_service.get_by_id(db, user.rank_id)

        if user_rank.order >= rank.order:
            raise ForbiddenException(detail=f"You can not increase rank to {rank.name}")

    def handle_filter(self, db: Session, user_query: Query[Any]):
        max_rank = rank_service.get_max_rank(db)
        return user_query.filter(User.rank_id != max_rank.id)


handler = IncreaseRankHandler()

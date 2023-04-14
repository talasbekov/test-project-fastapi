from sqlalchemy.orm import Session

from models import User
from .base import BaseHandler
from services import rank_service, history_service
from exceptions import ForbiddenException


class DecreaseRankHandler(BaseHandler):
    __handler__ = "decrease_rank"

    def handle_action(
        self, db: Session, user: User, action: dict, template_props: dict, props: dict
    ):
        tagname = action["rank"]["tagname"]
        rank = rank_service.get_by_id(db, props[tagname]["value"])
        if user.rank.order <= rank.order:
            raise ForbiddenException(detail=f"You can not decrease rank to {rank.name}")
        user.rank = rank
        history_service.create_history(db, user.id, rank)

        db.add(user)
        db.flush()

        return user


handler = DecreaseRankHandler()

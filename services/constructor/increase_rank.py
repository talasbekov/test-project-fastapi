from sqlalchemy.orm import Session

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
        print(props)
        rank = rank_service.get_by_id(db, props[tagname]["value"])
        user_rank = rank_service.get_by_id(db, user.rank_id)

        if user_rank.order >= rank.order:
            raise ForbiddenException(detail=f"You can not increase rank to {rank.name}")
        user.rank = rank
        history = rank_service.find_last_history(db, user.id)
        res = history_service.create_history(db, user.id, rank)
        document.old_history = history
        res.document_link = configs.GENERATE_IP + str(document.id)
        db.add(user)
        db.add(res)
        db.flush()

        return user


handler = IncreaseRankHandler()

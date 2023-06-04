from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from .base import BaseAutoTagHandler
from models import EmergencyServiceHistory
from schemas import AutoTagRead
from services import history_service
from utils import convert_days


class WorkMonthAutoTagHandler(BaseAutoTagHandler):
    __handler__ = "length-of-work-month"

    def handle(self, db: Session, user_id: UUID):
        histories = history_service._get_all_by_type_and_user_id(
            db, EmergencyServiceHistory.__mapper_args__["polymorphic_identity"], user_id
        ).all()
        min_date = datetime.min
        max_date = datetime.max
        for i in histories:
            if i.date_from < min_date:
                min_date = i.date_from
            if i.date_to > max_date:
                max_date = i.date_to
        if min_date != datetime.min:
            res = max_date - min_date
        else:
            return AutoTagRead(name=0, nameKZ=0)
        res = max_date - min_date
        _, months, _ = convert_days(res.days)
        return AutoTagRead(name=months, nameKZ=months)


handler = WorkMonthAutoTagHandler()

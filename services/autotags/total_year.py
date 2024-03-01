from uuid import UUID

from sqlalchemy.orm import Session

from .base import BaseAutoTagHandler
from models import EmergencyServiceHistory
from schemas import AutoTagRead
from services import history_service
from utils import convert_days


class TotalYearAutoTagHandler(BaseAutoTagHandler):
    __handler__ = "total-of-service-year"

    def handle(self, db: Session, user_id: UUID):
        histories = history_service._get_all_by_type_and_user_id(
            db, EmergencyServiceHistory.__mapper_args__[
                "polymorphic_identity"], user_id
        ).all()
        res = 0
        for i in histories:
            res = ((i.date_to - i.date_from).days * i.coefficient) + res
        years, _, _ = convert_days(res)
        return AutoTagRead(name=years, nameKZ=years)


handler = TotalYearAutoTagHandler()

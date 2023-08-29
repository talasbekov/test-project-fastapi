from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func

from models import Day
from schemas import DayCreate, DayUpdate
from services.base import ServiceBase


class DayService(ServiceBase[Day,
                             DayCreate,
                             DayUpdate]):
    def get_day_by_name(self, db: Session, name: List[str]):
        day = (db.query(Day)
               .filter(func.to_char(Day.name) == name)
               .order_by(Day.created_at.desc())
               .first())
        return day


day_service = DayService(Day)

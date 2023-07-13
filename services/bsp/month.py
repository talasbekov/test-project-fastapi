from typing import List

from sqlalchemy.orm import Session

from models import Month
from schemas import MonthCreate, MonthUpdate
from services.base import ServiceBase


class MonthService(ServiceBase[Month,
                               MonthCreate,
                               MonthUpdate]):
    def get_months_by_names(self, db: Session, names: List[str]):
        months = (db.query(Month)
                 .filter(Month.name.in_(names))
                 .order_by(Month.created_at.desc())
                 .all())
        return months

month_service = MonthService(Month)

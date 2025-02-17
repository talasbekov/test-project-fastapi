from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func

from models import Month
from schemas import MonthCreate, MonthUpdate
from services.base import ServiceBase


class MonthService(ServiceBase[Month,
                               MonthCreate,
                               MonthUpdate]):
    def get_months_by_names(self, db: Session, names: List[str]):
        months = (db.query(Month)
                 .filter(func.to_char(Month.name).in_(names))
                 .order_by(Month.created_at.desc())
                 .all())
        return months

    def get_month_by_order(self, db: Session, order: int):
        month = (db.query(Month)
                  .filter(Month.month_order == order)
                  .order_by(Month.created_at.desc())
                  .first())
        return month

month_service = MonthService(Month)

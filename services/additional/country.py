from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Country
from schemas import CountryCreate, CountryUpdate
from services.base import ServiceBase


class CountryService(ServiceBase[Country, CountryCreate, CountryUpdate]):

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Country]:
        return (db.query(Country)
                  .order_by(func.to_char(Country.name))
                  .offset(skip)
                  .limit(limit)
                  .all())

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(
                detail=f"Violation with id: {id} is not found!")
        return rank


country_service = CountryService(Country)

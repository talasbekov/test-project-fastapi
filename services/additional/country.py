from typing import List

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Country
from schemas import CountryCreate, CountryUpdate
from services.base import ServiceBase


class CountryService(ServiceBase[Country, CountryCreate, CountryUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        countries = db.query(Country)

        if filter != '':
            countries = self._add_filter_to_query(countries, filter)

        countries = (countries
                     .order_by(func.to_char(Country.name))
                     .offset(skip)
                     .limit(limit)
                     .all())

        total = db.query(Country).count()

        return {'total': total, 'objects': countries}

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(
                detail=f"Violation with id: {id} is not found!")
        return rank

    def _add_filter_to_query(self, country_query, filter):
        key_words = filter.lower().split()
        countries = (
            country_query
            .filter(
                and_(func.concat(func.concat(func.lower(Country.name), ' '),
                                 func.concat(func.lower(Country.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return countries

country_service = CountryService(Country)

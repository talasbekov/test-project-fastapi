from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Country
from schemas import CountryCreate, CountryUpdate
from services.base import ServiceBase
from services.filter import add_filter_to_query


class CountryService(ServiceBase[Country, CountryCreate, CountryUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        countries = db.query(Country)

        if filter != '':
            countries = add_filter_to_query(countries, filter, Country)

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


country_service = CountryService(Country)

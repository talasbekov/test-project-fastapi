from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Country
from schemas import CountryCreate, CountryUpdate
from services.base import ServiceBase


class CountryService(ServiceBase[Country, CountryCreate, CountryUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(detail=f"Violation with id: {id} is not found!")
        return rank


country_service = CountryService(Country)

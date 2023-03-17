from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import SportDegree
from schemas import SportDegreeCreate, SportDegreeUpdate
from services.base import ServiceBase


class SportDegreeService(ServiceBase[SportDegree, SportDegreeCreate, SportDegreeUpdate]):

    def get_by_id(self, db: Session, id: str):
        sport_degree = super().get(db, id)
        if sport_degree is None:
            raise NotFoundException(detail=f"SportDegree with id: {id} is not found!")
        return sport_degree


sport_degree_service = SportDegreeService(SportDegree)

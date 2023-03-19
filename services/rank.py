from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Rank
from schemas import RankCreate, RankUpdate
from .base import ServiceBase


class RankService(ServiceBase[Rank, RankCreate, RankUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(detail=f"Rank with id: {id} is not found!")
        return rank


rank_service = RankService(Rank)

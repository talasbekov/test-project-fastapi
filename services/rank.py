from sqlalchemy.orm import Session

from .base import ServiceBase

from models import Rank
from schemas import RankCreate, RankUpdate, RankRead
from exceptions.client import NotFoundException


class RankService(ServiceBase[Rank, RankCreate, RankUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(detail=f"Rank with id: {id} is not found!")
        return rank


rank_service = RankService(Rank)

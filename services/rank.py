import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Rank, RankHistory
from schemas import RankCreate, RankUpdate, RankRead
from .base import ServiceBase


class RankService(ServiceBase[Rank, RankCreate, RankUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(detail=f"Rank with id: {id} is not found!")
        return rank
    
    def get_by_option(self, db: Session, type: str, id: uuid.UUID, skip: int, limit: int):
        return [RankRead.from_orm(rank).dict() for rank in super().get_multi(db, skip, limit)]
    
    def get_object(self, db: Session, id: str):
        return self.get(db, id)

    def find_last_history(self, db: Session, user_id: uuid.UUID):
        return (
            db.query(RankHistory)
            .filter(
                RankHistory.user_id == user_id,
                RankHistory.date_to == None,
            )
            .order_by(RankHistory.date_from.desc())
            .first()
        )


rank_service = RankService(Rank)

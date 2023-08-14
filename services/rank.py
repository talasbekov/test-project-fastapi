import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Rank, RankHistory, User
from schemas import RankCreate, RankUpdate, RankRead

from .base import ServiceBase


class RankService(ServiceBase[Rank, RankCreate, RankUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(detail=f"Rank with id: {id} is not found!")
        return rank

    def get_by_option(self, db: Session, type: str,
                      id: str, skip: int, limit: int):
        user = db.query(User).filter(User.id == id).first()
        if user is None:
            raise NotFoundException(detail=f"User with id: {id} is not found!")
        if type == "write":
            return [RankRead.from_orm(rank).dict() for rank in db.query(Rank).filter(
                Rank.rank_order <= user.staff_unit.position.max_rank.rank_order).all()]
        else:
            if user.rank.rank_order == 1:
                return []
            else:
                return [self.get_by_order(db, user.rank.rank_order- 1)]

    def get_object(self, db: Session, id: str, type: str):
        return self.get(db, id)

    def find_last_history(self, db: Session, user_id: str):
        return (
            db.query(RankHistory)
            .filter(
                RankHistory.user_id == user_id,
                RankHistory.date_to == None,
            )
            .order_by(RankHistory.date_from.desc())
            .first()
        )

    def get_max_rank(self, db: Session):
        return (
            db.query(Rank).order_by(Rank.rank_order.desc()).limit(1).first()
        )

    def get_min_rank(self, db: Session):
        return (
            db.query(Rank).order_by(Rank.rank_order.asc()).limit(1).first()
        )

    def get_by_order(self, db: Session, order: int):
        res = db.query(Rank).filter(Rank.rank_order == order).first()
        if res is None:
            raise NotFoundException("Rank with order: {order} is not found!")
        return res


rank_service = RankService(Rank)

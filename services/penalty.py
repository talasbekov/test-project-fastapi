import uuid
from datetime import datetime

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Penalty, PenaltyType, PenaltyHistory
from schemas import PenaltyCreate, PenaltyUpdate, PenaltyTypeRead, PenaltyReadForOption
from .base import ServiceBase


class PenaltyService(ServiceBase[Penalty, PenaltyCreate, PenaltyUpdate]):
    def create_relation(self, db: Session, user_id: str,
                        type_id: str):
        penalty = super().create(db, PenaltyCreate(type_id=type_id, user_id=user_id))
        return penalty

    def get_by_id(self, db: Session, id: str) -> Penalty:
        res = self.get(db, str(id))
        if res is None:
            raise NotFoundException(
                detail=f"{self.model.__name__} with id {id} not found!")
        return res


    def get_by_type_and_user(self, db: Session, type_id: str, user_id: str) -> Penalty:
        res = (
               db.query(Penalty)
               .filter(Penalty.user_id == user_id)
               .filter(Penalty.type_id == type_id)
              )
        return res

    
    def get_by_option(
        self, db: Session, type: str, id: str, skip: int, limit: int
    ):
        if type == "write":
            return [
                PenaltyTypeRead.from_orm(i).dict()
                for i in db.query(PenaltyType).offset(skip).limit(limit).all()
            ]
        else:
            penalties = (
                db.query(Penalty)
                .filter(Penalty.user_id == id)
                .join(
                    PenaltyHistory,
                    and_(PenaltyHistory.user_id == id,
                         PenaltyHistory.date_to > datetime.now()
                         )
                )
            )
            penalties_with_names = []
            for penalty in penalties:
                penalty_with_name = PenaltyReadForOption.from_orm(penalty).dict()
                penalty_with_name['name'] = penalty.type.name
                penalty_with_name['nameKZ'] = penalty.type.nameKZ
                penalties_with_names.append(penalty_with_name)
            return penalties_with_names

    def get_object(self, db: Session, id: str, type: str):
        if type == "write":
            return db.query(PenaltyType).filter(PenaltyType.id == id).first()
        else:
            return db.query(Penalty).filter(Penalty.id == id).first().type

    def stop_relation(self, db: Session, user_id: str, id: str):
        # penalty = self.get_by_type_and_user(id, user_id)
        penalty_history = (
            db.query(PenaltyHistory)
            .filter(
                PenaltyHistory.penalty_id == id,
                PenaltyHistory.user_id == user_id
            ).first()
        )
        if penalty_history is None:
            raise NotFoundException(
                detail=f"Penalty with id: {id} is not found!")
        penalty_history.date_to = datetime.now()
        db.add(penalty_history)
        db.flush()
        return penalty_history

    def exists_relation(self, db: Session, user_id: str, id: str):
        return (
            db.query(Penalty)
            .filter(Penalty.user_id == user_id)
            .filter(Penalty.id == id)
            .first()
        ) is not None


penalty_service = PenaltyService(Penalty)

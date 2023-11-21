from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import RecommenderUser
from schemas import RecommenderUserCreate, RecommenderUserUpdate
from .base import ServiceBase


class RecommenderUserService(
        ServiceBase[RecommenderUser, RecommenderUserCreate, RecommenderUserUpdate]):

    def get_by_id(self, db: Session, id: str):
        recommender_user = super().get(db, id)
        if recommender_user is None:
            raise NotFoundException(
                detail=f"Recommender User with id: {id} is not found!")
        return recommender_user

    def get_by_user_id(self, db: Session, user_id: str):
        recommender_user = db.query(
            self.model).filter(
            self.model.user_id == user_id).first()
        if recommender_user is None:
            return None
        return recommender_user

    def get_by_user_id_and_date(self, db: Session, user_id: str, date_till):
        recommender_user = db.query(
            self.model).filter(
            self.model.user_id == user_id,
            self.model.created_at <= date_till
        ).first()
        if recommender_user is None:
            return None
        return recommender_user


recommender_user_service = RecommenderUserService(RecommenderUser)

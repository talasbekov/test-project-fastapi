import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import RecommenderUser
from schemas import RecommenderUserCreate, RecommenderUserUpdate, RecommenderUserRead
from .base import ServiceBase


class RecommenderUserService(ServiceBase[RecommenderUser, RecommenderUserCreate, RecommenderUserUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(detail=f"Rank with id: {id} is not found!")
        return rank
    

recommender_user_service = RecommenderUserService(RecommenderUser)


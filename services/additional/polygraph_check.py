from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import PolygraphCheck, Profile
from schemas import PolygraphCheckCreate, PolygraphCheckUpdate
from services import profile_service
from services.base import ServiceBase


class PolygraphCheckService(
        ServiceBase[PolygraphCheck, PolygraphCheckCreate, PolygraphCheckUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(
                detail=f"Violation with id: {id} is not found!")
        return rank

    def create(self, db: Session, obj_in: PolygraphCheckCreate):
        return super().create(db, obj_in)

    def update(self, db: Session, db_obj: PolygraphCheck,
               obj_in: PolygraphCheckUpdate):
        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def delete(self, db: Session, id: str):
        return super().remove(db, id)

    def get_multi_by_user_id(
            self, db: Session, user_id: str, skip: int = 0, limit: int = 100):
        profile: Profile = profile_service.get_by_user_id(db, user_id)
        if profile is None:
            raise NotFoundException(
                detail=f"Profile with user_id: {user_id} is not found!")

        polygraph_checks = db.query(self.model).filter(
            self.model.profile_id == profile.additional_profile.id
        ).offset(skip).limit(limit).all()

        return polygraph_checks


polyhraph_check_service = PolygraphCheckService(PolygraphCheck)

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import AbroadTravel, Profile
from schemas import AbroadTravelCreate, AbroadTravelUpdate
from services import profile_service
from services.base import ServiceBase


class AbroadTravelService(
        ServiceBase[AbroadTravel, AbroadTravelCreate, AbroadTravelUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(
                detail=f"Violation with id: {id} is not found!")
        return rank

    def create(self, db: Session, obj_in: AbroadTravelCreate):
        return super().create(db, obj_in)

    def update(self, db: Session, db_obj: AbroadTravel,
               obj_in: AbroadTravelUpdate):
        return super().update(db, db_obj, obj_in)

    def delete(self, db: Session, id: str):
        return super().delete(db, id)

    def get_multi_by_additional_profile_id(self, db: Session, profile_id: str):
        qry = db.query(
            self.model).filter(
            self.model.profile_id == profile_id).all()
        return qry

    def get_multi_by_user_id(
            self, db: Session, user_id: str, skip: int = 0, limit: int = 100):
        profile: Profile = profile_service.get_by_user_id(db, user_id)
        abroad_travels = db.query(self.model).filter(
            self.model.profile_id == profile.additional_profile.id
        ).offset(skip).limit(limit).all()
        return abroad_travels


abroad_travel_service = AbroadTravelService(AbroadTravel)

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import AbroadTravel
from services.base import ServiceBase
from schemas import AbroadTravelCreate, AbroadTravelUpdate

class AbroadTravelService(ServiceBase[AbroadTravel, AbroadTravelCreate, AbroadTravelUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(detail=f"Violation with id: {id} is not found!")
        return rank
    
    def create(self, db: Session, obj_in: AbroadTravelCreate):
        return super().create(db, obj_in)
    
    def update(self, db: Session, db_obj: AbroadTravel, obj_in: AbroadTravelUpdate):
        return super().update(db, db_obj, obj_in)
    
    def delete(self, db: Session, id: str):
        return super().delete(db, id)


abroad_travel_service = AbroadTravelService(AbroadTravel)

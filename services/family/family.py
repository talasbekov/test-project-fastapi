from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Family
from schemas import FamilyCreate, FamilyUpdate
from services import ServiceBase


class FamilyService(ServiceBase[Family, FamilyCreate, FamilyUpdate]):
    
    def get_by_id(self, db: Session, id: str) -> Family:
        family = db.query(Family).filter(Family.id == id).first()
        if not family:
            raise NotFoundException("Family with id: {id} not found!")
        return family


family_service = FamilyService(Family)

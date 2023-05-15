from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Family
from schemas import FamilyCreate, FamilyUpdate
from services import ServiceBase


class FamilyService(ServiceBase[Family, FamilyCreate, FamilyUpdate]):
    
    def get_by_id(self, db: Session, id: str) -> Family:
        family = db.query(Family).filter(Family.id == id).first()
        if not family:
            raise NotFoundException(f"Family with id: {id} not found!")
        return family
    
    def get_by_relation_id(self, db: Session, relation_id: str):
        family = db.query(Family).filter(Family.relation_id == relation_id).first()
        
        return family


family_service = FamilyService(Family)

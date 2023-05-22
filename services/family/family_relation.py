from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import FamilyRelation
from schemas import FamilyRelationCreate, FamilyRelationUpdate
from services import ServiceBase


class FamilyRelationService(ServiceBase[FamilyRelation, FamilyRelationCreate, FamilyRelationUpdate]):

    def get_by_id(self, db: Session, id: str) -> FamilyRelation:
        family_relation = db.query(FamilyRelation).filter(FamilyRelation.id == id).first()
        if not family_relation:
            raise NotFoundException(f"FamilyRelation with id: {id} not found!")
        return family_relation
    
    def get_by_name(self, db: Session, name: str):
        family_relation = db.query(FamilyRelation).filter(FamilyRelation.name == name).first()
        if not family_relation:
            raise NotFoundException(f"FamilyRelation with name: {name} not found!")
        return family_relation


family_relation_service = FamilyRelationService(FamilyRelation)

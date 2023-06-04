from typing import List
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Family
from schemas import FamilyCreate, FamilyUpdate, FamilyRead
from services import ServiceBase


class FamilyService(ServiceBase[Family, FamilyCreate, FamilyUpdate]):
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Family]:
        families = db.query(Family).join(Family.violation).join(Family.abroad_travel).offset(skip).limit(limit).all()

        return families

    def get_by_id(self, db: Session, id: str) -> Family:
        family = db.query(Family).join(Family.violation).join(Family.abroad_travel).filter(Family.id == id).first()
        if not family:
            raise NotFoundException(f"Family with id: {id} not found!")
        return family

    def get_by_relation_id(self, db: Session, relation_id: str):
        family = db.query(Family).filter(Family.relation_id == relation_id).first()
        return family


family_service = FamilyService(Family)

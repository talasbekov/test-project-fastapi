from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import FamilyRelation
from schemas import FamilyRelationCreate, FamilyRelationUpdate
from services import ServiceBase
from services.filter import add_filter_to_query


class FamilyRelationService(
        ServiceBase[FamilyRelation, FamilyRelationCreate, FamilyRelationUpdate]):
    
    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        family_relations = db.query(FamilyRelation)

        if filter != '':
            family_relations = add_filter_to_query(family_relations, filter, FamilyRelation)

        family_relations = (family_relations
                       .order_by(func.to_char(FamilyRelation.name))
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = db.query(FamilyRelation).count()

        return {'total': total, 'objects': family_relations}

    def get_by_id(self, db: Session, id: str) -> FamilyRelation:
        family_relation = db.query(FamilyRelation).filter(
            FamilyRelation.id == id).first()
        if not family_relation:
            raise NotFoundException(f"FamilyRelation with id: {id} not found!")
        return family_relation

    def get_by_name(self, db: Session, name: str):
        family_relation = db.query(FamilyRelation).filter(
            FamilyRelation.name == name).first()
        if not family_relation:
            raise NotFoundException(
                f"FamilyRelation with name: {name} not found!")
        return family_relation


family_relation_service = FamilyRelationService(FamilyRelation)

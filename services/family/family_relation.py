from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import FamilyRelation
from schemas import FamilyRelationCreate, FamilyRelationUpdate
from services import ServiceBase


class FamilyRelationService(
        ServiceBase[FamilyRelation, FamilyRelationCreate, FamilyRelationUpdate]):
    
    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        family_relations = db.query(FamilyRelation)

        if filter != '':
            family_relations = self._add_filter_to_query(family_relations, filter)

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
    
    def _add_filter_to_query(self, family_relation_query, filter):
        key_words = filter.lower().split()
        family_relations = (
            family_relation_query
            .filter(
                and_(func.concat(func.concat(func.lower(FamilyRelation.name), ' '),
                                 func.concat(func.lower(FamilyRelation.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return family_relations


family_relation_service = FamilyRelationService(FamilyRelation)

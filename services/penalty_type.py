from sqlalchemy import func, and_

from models import PenaltyType
from sqlalchemy.orm import Session
from schemas import PenaltyTypeCreate, PenaltyTypeUpdate
from .base import ServiceBase


class PenaltyTypeService(ServiceBase[PenaltyType, PenaltyTypeCreate, PenaltyTypeUpdate]):
    
    def get_all(self, db: Session,
                    skip: int,
                    limit: int,
                    filter: str = ''):
        penalty_types = db.query(PenaltyType)

        if filter != '':
            penalty_types = self._add_filter_to_query(penalty_types, filter)

        penalty_types = (penalty_types
                       .order_by(PenaltyType.name)
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = (db.query(PenaltyType).count())
        
        return {'total': total, 'objects': penalty_types}
    
    def _add_filter_to_query(self, penalty_type_query, filter):
        key_words = filter.lower().split()
        penalty_types = (
            penalty_type_query
            .filter(
                and_(func.concat(func.concat(func.lower(PenaltyType.name), ' '),
                                 func.concat(func.lower(PenaltyType.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return penalty_types

penalty_type_service = PenaltyTypeService(PenaltyType)

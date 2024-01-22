from sqlalchemy import func, and_

from models import PenaltyType
from sqlalchemy.orm import Session
from schemas import PenaltyTypeCreate, PenaltyTypeUpdate
from utils import add_filter_to_query
from .base import ServiceBase


class PenaltyTypeService(ServiceBase[PenaltyType, PenaltyTypeCreate, PenaltyTypeUpdate]):
    
    def get_all(self, db: Session,
                    skip: int,
                    limit: int,
                    filter: str = ''):
        penalty_types = db.query(PenaltyType)

        if filter != '':
            penalty_types = add_filter_to_query(penalty_types, filter, PenaltyType)

        penalty_types = (penalty_types
                       .order_by(PenaltyType.name)
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = (db.query(PenaltyType).count())
        
        return {'total': total, 'objects': penalty_types}


penalty_type_service = PenaltyTypeService(PenaltyType)

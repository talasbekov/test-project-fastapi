from models import PenaltyType
from sqlalchemy.orm import Session
from schemas import PenaltyTypeCreate, PenaltyTypeUpdate
from .base import ServiceBase


class PenaltyTypeService(ServiceBase[PenaltyType, PenaltyTypeCreate, PenaltyTypeUpdate]):
    
    def get_multi(self, db: Session,
                    skip: int,
                    limit: int):

        penalty_types = (db.query(PenaltyType)
                        .order_by(PenaltyType.created_at.desc())
                        .offset(skip)
                        .limit(limit)
                        .all())

        total = (db.query(PenaltyType).count())

        return {'total': total, 'objects': penalty_types}

penalty_type_service = PenaltyTypeService(PenaltyType)

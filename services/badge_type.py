from sqlalchemy.orm import Session

from models import BadgeType
from schemas import BadgeTypeCreate, BadgeTypeUpdate
from .base import ServiceBase


class BadgeTypeService(ServiceBase[BadgeType, BadgeTypeCreate, BadgeTypeUpdate]):
  
    def get_multi(self, db: Session,
                    skip: int,
                    limit: int):

        badge_types = (db.query(BadgeType).order_by(self.model.created_at.desc()).offset(skip).limit(limit).all())

        total = (db.query(BadgeType).count())

        return {'total': total, 'objects': badge_types}


badge_type_service = BadgeTypeService(BadgeType)

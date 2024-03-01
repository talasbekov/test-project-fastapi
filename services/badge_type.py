from sqlalchemy.orm import Session

from models import BadgeType
from schemas import BadgeTypeCreate, BadgeTypeUpdate
from services.filter import add_filter_to_query
from .base import ServiceBase


class BadgeTypeService(ServiceBase[BadgeType, BadgeTypeCreate, BadgeTypeUpdate]):

    def get_all(self, db: Session,
                  skip: int,
                  limit: int,
                  filter: str = ''
                  ):
        print("here1")
        badge_types = db.query(BadgeType)
        # print(badge_types.all())
        print("here2")
        if filter != '':
            badge_types = add_filter_to_query(badge_types, filter, BadgeType)
        print("here3")
        badge_types = (badge_types
                       .order_by(BadgeType.name)
                       .offset(skip)
                       .limit(limit)
                       .all())
                       
        print("here4")
        total = (db.query(BadgeType).count())
        print("here5")  
        return {'total': total, 'objects': badge_types}


badge_type_service = BadgeTypeService(BadgeType)

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from models import BadgeType
from schemas import BadgeTypeCreate, BadgeTypeUpdate
from .base import ServiceBase


class BadgeTypeService(ServiceBase[BadgeType, BadgeTypeCreate, BadgeTypeUpdate]):

    def get_all(self, db: Session,
                  skip: int,
                  limit: int,
                  filter: str = ''
                  ):
        badge_types = db.query(BadgeType)

        if filter != '':
            badge_types = self._add_filter_to_query(badge_types, filter)

        badge_types = (badge_types
                       .order_by(BadgeType.name)
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = (db.query(BadgeType).count())

        return {'total': total, 'objects': badge_types}

    def _add_filter_to_query(self, badge_type_query, filter):
        key_words = filter.lower().split()
        badge_types = (
            badge_type_query
            .filter(
                and_(func.concat(func.concat(func.lower(BadgeType.name), ' '),
                                func.concat(func.lower(BadgeType.nameKZ), ' '))
                    .contains(name) for name in key_words)
            )
        )
        return badge_types


badge_type_service = BadgeTypeService(BadgeType)

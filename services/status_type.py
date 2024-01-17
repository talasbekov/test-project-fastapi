from sqlalchemy import and_, func

from models import StatusType
from schemas import StatusTypeCreate, StatusTypeUpdate
from .base import ServiceBase
from typing import List

from sqlalchemy.orm import Session


class StatusTypeService(
        ServiceBase[StatusType, StatusTypeCreate, StatusTypeUpdate]):
    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        status_types = (db.query(StatusType))

        if filter != '':
            status_types = self._add_filter_to_query(status_types, filter)

        status_types = (status_types
                        .offset(skip)
                        .limit(limit)
                        .all())

        count = db.query(StatusType).count()

        return {"total": count, "objects": status_types}

    def _add_filter_to_query(self, status_type_query, filter):
        key_words = filter.lower().split()
        status_types = (
            status_type_query
            .filter(
                and_(func.concat(func.concat(func.lower(StatusType.name), ' '),
                                 func.concat(func.lower(StatusType.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return status_types

status_type_service = StatusTypeService(StatusType)

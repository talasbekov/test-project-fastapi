from sqlalchemy import and_, func

from models import StatusType
from schemas import StatusTypeCreate, StatusTypeUpdate
from utils import add_filter_to_query
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
            status_types = add_filter_to_query(status_types, filter, StatusType)

        status_types = (status_types
                        .offset(skip)
                        .limit(limit)
                        .all())

        count = db.query(StatusType).count()

        return {"total": count, "objects": status_types}


status_type_service = StatusTypeService(StatusType)
